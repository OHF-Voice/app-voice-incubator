# Home Assistant App: Voice Incubator

Source repository of the [Voice Incubator][docs] app for Home Assistant. The
app's own source is [OHF-Voice/voice-incubator][source]: this repository
builds a release of it into the app.

## Releases

Not published yet: where the app is installed from is still to be decided.

## Local build

```sh
docker build -t local/app-voice-incubator voice_labs
```

This builds the release `voice_labs/Dockerfile` pins
(`VOICE_INCUBATOR_VERSION`). To build a checkout of the source instead, write
it beside the Dockerfile first, from that checkout:

```sh
scripts/app_source.sh ~/opt/app-voice-incubator/voice_labs
```

## Related

- [voice-incubator][source]: the app's source.
- [integration-voice-incubator][integration]: its Home Assistant integration,
  installed with HACS, and the guide.
- [firmware-voice-incubator][firmware]: the satellites' ESPHome firmware, and
  the protocol they speak.

[docs]: voice_labs/DOCS.md
[source]: https://github.com/OHF-Voice/voice-incubator
[integration]: https://github.com/OHF-Voice/integration-voice-incubator
[firmware]: https://github.com/OHF-Voice/firmware-voice-incubator
