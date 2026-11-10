# Base image updated by Renovate, update versionCompatibility on a base bump
ARG BUILD_FROM=ghcr.io/home-assistant/base-debian:trixie-2026.11.0@sha256:d996c8f8ef0096a1ac3756766149b31b8171afc663068cc192f2bcab20f1b8c9

# The app is built from a release of its source, OHF-Voice/voice-incubator, in
# the steps its own (standalone) Dockerfile takes: a change there belongs here
# too. What is compiled -- adapt-ctc's searches, the wake verifier's decoder,
# FluidSynth -- and the Python packages are built in the first stages, so the
# image has no compiler. TRAINING=false leaves out wake word training
# (TensorFlow, 2 GB).

FROM ${BUILD_FROM} AS build-base
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        libopenblas-dev \
        libsndfile1-dev \
        pkg-config \
        python3 \
        python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# FluidSynth plays the call's sounds (voice_incubator/instruments.py): only its
# synth, so without the audio drivers Debian's is built with -- SDL, which
# brings Mesa and LLVM (200 MB), PulseAudio, PipeWire, JACK. libsndfile reads
# the SoundFont's compressed samples.
ARG FLUIDSYNTH_VERSION=2.6.1
ARG FLUIDSYNTH_SHA256=3d258a3bf97cc20c59eeebfe62c2432fae88adda74d3ad098681c76e0ebf446b
RUN \
    curl -sSfL -o /tmp/fluidsynth.tar.gz \
        "https://github.com/FluidSynth/fluidsynth/archive/refs/tags/v${FLUIDSYNTH_VERSION}.tar.gz" \
    && echo "${FLUIDSYNTH_SHA256}  /tmp/fluidsynth.tar.gz" | sha256sum -c - \
    && mkdir /tmp/fluidsynth && tar xzf /tmp/fluidsynth.tar.gz -C /tmp/fluidsynth --strip-components 1 \
    && cmake -S /tmp/fluidsynth -B /tmp/fluidsynth/build -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_INSTALL_LIBDIR=lib \
        -Denable-alsa=off -Denable-aufile=off -Denable-dbus=off -Denable-ipv6=off \
        -Denable-jack=off -Denable-ladspa=off -Denable-libinstpatch=off -Denable-midishare=off \
        -Denable-network=off -Denable-oss=off -Denable-pipewire=off -Denable-portaudio=off \
        -Denable-pulseaudio=off -Denable-readline=off -Denable-sdl3=off -Denable-systemd=off \
        -Denable-signalsmith=off -Denable-libsndfile=on \
    && cmake --build /tmp/fluidsynth/build -j "$(nproc)" \
    && cmake --install /tmp/fluidsynth/build \
    && rm -rf /tmp/fluidsynth /tmp/fluidsynth.tar.gz /usr/local/bin/fluidsynth /usr/local/include /usr/local/share


# The source: the release pinned here, or a checkout's -- voice-incubator.tar.gz
# beside this file, which the source's scripts/app_source.sh writes.
FROM build-base AS source
ARG VOICE_INCUBATOR_VERSION=0.2.0

WORKDIR /usr/src/voice_incubator
COPY Dockerfile voice-incubator*.tar.gz /tmp/source/
RUN \
    if [ -f /tmp/source/voice-incubator.tar.gz ]; then \
        tar xzf /tmp/source/voice-incubator.tar.gz --strip-components 1; \
    else \
        curl -sSfL \
            "https://github.com/OHF-Voice/voice-incubator/archive/refs/tags/v${VOICE_INCUBATOR_VERSION}.tar.gz" \
            | tar xz --strip-components 1; \
    fi \
    && rm -rf /tmp/source


FROM build-base AS builder
ARG BUILD_ARCH
ARG TRAINING=true

WORKDIR /usr/src/voice_incubator

COPY --from=source /usr/src/voice_incubator/requirements.txt /usr/src/voice_incubator/requirements-training.txt ./
RUN \
    pip3 install --no-cache-dir -U --ignore-installed setuptools wheel \
    && pip3 install --no-cache-dir -r requirements.txt \
    && if [ "${TRAINING}" = "true" ]; then pip3 install --no-cache-dir -r requirements-training.txt; fi

# What the image carries besides its code (voice_incubator/downloads.py, IMAGE):
# the speaker, wake word and Kaldi models, and Kaldi's tools for this
# architecture, each checked against its SHA-256.
COPY --from=source /usr/src/voice_incubator/voice_incubator/__init__.py /usr/src/voice_incubator/voice_incubator/downloads.py ./voice_incubator/
RUN python3 -m voice_incubator.downloads fetch models --arch "${BUILD_ARCH:-$(dpkg --print-architecture | sed 's/arm64/aarch64/')}"

# The wake verifier's resident decoder, compiled against those tools; then
# only what the verifier, the decoder and phonetisaurus (Kaldi mode's guessed
# pronunciations) use of them is kept (wyoming_wake_kaldi/prune.py).
COPY --from=source \
    /usr/src/voice_incubator/wyoming_wake_kaldi/__init__.py \
    /usr/src/voice_incubator/wyoming_wake_kaldi/kaldi.py \
    /usr/src/voice_incubator/wyoming_wake_kaldi/prune.py \
    ./wyoming_wake_kaldi/
COPY --from=source /usr/src/voice_incubator/wyoming_wake_kaldi/decoderd ./wyoming_wake_kaldi/decoderd
RUN \
    mkdir -p models/wake-kaldi-decoderd \
    && bash wyoming_wake_kaldi/decoderd/build.sh "$PWD/models/wake-kaldi-tools" "$PWD/models/wake-kaldi-decoderd/verify_decoderd" \
    && rm -rf models/wake-kaldi-decoderd/.fst_shadow_include \
    && python3 -m wyoming_wake_kaldi.prune models/wake-kaldi-tools models/wake-kaldi-decoderd/verify_decoderd models/wake-kaldi-tools/phonetisaurus

# adapt-ctc's native searches (several times faster than the fallbacks).
COPY --from=source /usr/src/voice_incubator/setup.py ./
COPY --from=source /usr/src/voice_incubator/adapt_ctc ./adapt_ctc
RUN python3 setup.py build_ext --inplace && rm -rf build


# Perl: Kaldi's scripts, which build a wake word's graphs (Encode and the rest
# of Perl's modules, not only the minimal Perl Debian always has).
FROM ${BUILD_FROM}
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /usr/src/voice_incubator

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libgomp1 \
        libopenblas0 \
        libsndfile1 \
        musescore-general-soundfont-small \
        perl \
        python3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
RUN ldconfig
COPY --from=builder /usr/src/voice_incubator/models ./models
COPY --from=source /usr/src/voice_incubator/wake.yaml ./
COPY --from=source /usr/src/voice_incubator/sounds ./sounds
COPY --from=builder /usr/src/voice_incubator/adapt_ctc ./adapt_ctc
COPY --from=source /usr/src/voice_incubator/wyoming_wake_kaldi ./wyoming_wake_kaldi
COPY --from=source /usr/src/voice_incubator/sentence_stream ./sentence_stream
COPY --from=source /usr/src/voice_incubator/microwakeword ./microwakeword
COPY --from=source /usr/src/voice_incubator/voice_incubator ./voice_incubator
# Parakeet, EmbeddingGemma and GLiNER are downloaded into the app's data the
# first time it starts (voice_incubator/downloads.py), and Piper's voices the first
# time one is used (voice_incubator/piper_voices.py): linked from models/.
RUN python3 -m voice_incubator.downloads link /data/models

# Started by its s6 service, which reads its options from /data/options.json.
WORKDIR /
COPY rootfs /

HEALTHCHECK --start-period=10m \
    CMD curl -sf http://127.0.0.1:8099/health > /dev/null || exit 1

LABEL \
    org.opencontainers.image.title="Home Assistant App: Voice Incubator" \
    org.opencontainers.image.description="Voice satellites with your own commands, recognized on this machine" \
    org.opencontainers.image.source="https://github.com/OHF-Voice/app-voice-incubator" \
    org.opencontainers.image.licenses="Apache License 2.0"
