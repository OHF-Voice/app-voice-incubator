# Home Assistant App: Voice Incubator

Source repository of the [Voice Incubator][docs] app for Home Assistant. The
app's own source is [OHF-Voice/voice-incubator][source]: this repository
builds a release of it into the app.

## Install

[![Add the repository to your Home Assistant.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FOHF-Voice%2Fapp-voice-incubator)

Add `https://github.com/OHF-Voice/app-voice-incubator` to Home Assistant's app
repositories, then install **Voice Incubator**. Its
[install steps](https://github.com/OHF-Voice/voice-incubator#install) have the
integration and the satellites' firmware too.

## Releases

A published release builds and publishes the app's image,
`ghcr.io/ohf-voice/app-voice-incubator` (amd64 and aarch64), tagged with its
version ([Deploy](.github/workflows/deploy.yaml)): the release's tag is
`config.yaml`'s version. The source it builds is the release
`VOICE_INCUBATOR_VERSION` pins in the Dockerfile.

## Local build

```sh
docker build -t local/app-voice-incubator voice_incubator
```

This builds the release `voice_incubator/Dockerfile` pins
(`VOICE_INCUBATOR_VERSION`). To build a checkout of the source instead, write
it beside the Dockerfile first, from that checkout:

```sh
scripts/app_source.sh ~/opt/app-voice-incubator/voice_incubator
```

## Related

- [voice-incubator][source]: the app's source.
- [integration-voice-incubator][integration]: its Home Assistant integration,
  installed with HACS, and the guide.
- [firmware-voice-incubator][firmware]: the satellites' ESPHome firmware, and
  the protocol they speak.

[docs]: voice_incubator/DOCS.md
[source]: https://github.com/OHF-Voice/voice-incubator
[integration]: https://github.com/OHF-Voice/integration-voice-incubator
[firmware]: https://github.com/OHF-Voice/firmware-voice-incubator
