# Changelog

## 0.3.4

- **The web UI opens again.** Its port is now one the Supervisor picks
  instead of 8099, which another app on the host's network could hold.
  That change reached the app store before the app did, so 0.3.3
  installed or updated since then sent the web UI to a port nothing
  listened on: "502: Bad Gateway" (OHF-Voice/voice-incubator#25,
  OHF-Voice/app-voice-incubator#3).

## 0.3.3

- **Satellites stay connected on a weak Wi-Fi link.** Missed mDNS
  refreshes expired a satellite's record while it was still there, which
  ended its session; nothing reconnected until it was found again, ~50
  minutes in one report. A session now ends only on its own connection and
  keeps reconnecting to the last address it had, and a satellite whose
  name got no answer is asked again (OHF-Voice/voice-incubator#18).
- **Home Assistant restarting, or starting after the app, is waited for.**
  The app read it before its integrations were loaded: the integration
  stayed "not loaded" and the home's sentence triggers were missing until
  the app was restarted. Now nothing is read until Home Assistant says it
  has started (OHF-Voice/voice-incubator#15, OHF-Voice/voice-incubator#1).
- **Voice Incubator as its own conversation agent doesn't loop.** With the
  fallback agent set to Voice Incubator's Wyoming agent in Home Assistant,
  a sentence it didn't know was asked of itself again and again. It's now
  said "Sorry, I didn't understand that" once, with a warning in the log to
  choose another agent (OHF-Voice/voice-incubator#9).
- **The integration is installed from the Marketplace,** which HACS became
  in Home Assistant 2026.11, with no restart (OHF-Voice/voice-incubator#12).
- **The integration notice is shown once,** its state in plain words ("is
  not loaded in Home Assistant", not "not_loaded").
- **A device heard only in its area, said with that area elsewhere, says
  so:** "the Fan in the Office can only be controlled from there", not
  "there's no Fan here, only in the Office".
- **Sentence triggers win over an area's own commands as good as them,** as
  Home Assistant runs a trigger before its intents.
- **English:** "change the lights to blue" sets the color and color
  temperature; "what's the time" and "tell me the time" tell it, like the
  date.

## 0.3.2

- **Small boxes don't run out of memory building the home's sentences.**
  Every new sentence was embedded in one run of the model, and a run's
  memory grows with its size: 300 sentences added 713 MB, which got the
  app killed (signal 9) on an HA Blue right after loading embeddings. They
  now go 16 at a time.
- **Enrolling a speaker doesn't fail on a cut-off audio frame.** With its
  outgoing buffer nearly full, a device could end a frame halfway through
  a sample. Enrollment then failed with "buffer size must be a multiple of
  element size", and the rest of the audio was read a byte off. The half
  sample is now joined to the next frame.

## 0.3.1

- **Updating from 0.2 works.** The language now defaults to English, what
  0.2 spoke. 0.3.0 had no default, and the update failed: the Supervisor
  restarts the app after updating it, and refused to without a language.
  The app was updated all the same, and stopped; picking a language on its
  Configuration tab starts it again.
- **Enrolling a speaker no longer crashes on older x86 CPUs.** Silero VAD
  (pysilero-vad 3.4.0) needed AVX2, so on CPUs without it (many Celeron,
  Atom and Pentium boxes) the app exited with signal 4 as soon as Silero
  loaded: enrolling, and ending a command. pysilero-vad 3.4.1 picks the
  best instructions the CPU has when it loads.
- **Alarms take times as speech-to-text writes them.** "Five fifty" written
  as 5.50, "five oh one" as 5-0-1 and "five seventeen" as 517 set the alarm
  for that time; in a reminder they're times after "at" or "by", or before
  am or pm. "7 a.m." is 7 AM, not 7 PM. Times are said naturally: "5 PM",
  not "five zero zero P M", and ":07" as "oh seven".
- **Home Assistant devices with three-part identifiers don't break the
  connection.** Some integrations register them, which stopped the
  catalog from loading.
- **Free text keeps its last words.** Text that ends in "you" keeps it,
  "announce that I love it" ends on "it", and a "please" after it
  ("announce dinner is ready please") is left out instead of losing the
  command.

## 0.3.0

- **The app's language is picked on its Configuration tab, and it has no
  default.** Updated from 0.2, the app won't start until one is picked.
  German, Spanish, French, Italian, Dutch, Polish, Russian and Ukrainian
  now have English's commands, versions, slots, lists and actions, alarms
  and reminders on the calendar, and two commands said together. The
  language's speech model is downloaded at the first start. Piper's voices
  are the language's, and GLiNER is English only.
- **Wake word training is installed from the Wake words page.** TensorFlow
  is no longer in the image (3.0 GB down to 1.1 GB on amd64), and the
  training kit no longer has to be copied in by hand. Install downloads
  about 1.2 GB on amd64 and 900 MB on aarch64, and takes about 4 GB in the
  data folder. Remove frees it again. Updates keep it, and backups leave it
  out.
- **A training voice that won't download fails the training.** It used to
  wait without saying anything, trying again every 30 s; now the training
  stops after three tries and says why.
- **Wake words are trained with the new libritts_r voice.** It has 904
  speakers where the old one had 2306, with other ids. A saved speaker it
  no longer has speaks with the voice's default.
- **A command said right after the wake word isn't missed.** Silero now
  starts listening on the quiet before the wake word. Started on "okay",
  it scored a plainly said command 0.36, under the 0.5 that starts it,
  and the call ended "no speech was heard".
- **Adding from the library is quick.** The library's sentences are
  embedded in the background after the first build (100 s once on an HA
  Green), so adding 12 commands no longer takes 23 s. The Add buttons say
  "Adding…" until the commands are recognized.
- **The app's logo reads in dark mode too.** The Supervisor shows one logo
  for both themes, and its dark gray wordmark all but disappeared on a dark
  card; it is blue now.

## 0.2.1

- **Wake words are verified on the AEC capture.** The VPE's AGC capture
  sometimes sits about 35 dB down, and near misses ("okay natalie") got
  through on it. The command is still heard on the AGC capture; a call
  without AEC audio is verified as before, and `--wake-capture agc` puts it
  back for every call.
- **The second opinion doesn't overturn a near miss.** A wake word Kaldi
  refused is no longer accepted on the ratio when it sounds more like one of
  37 of "okay nabu"'s confusables ("okay natalie", "okay taboo" with a long
  last vowel) than like it. The call's trace says which.
- **Sentence triggers are known by their sentence.** An automation with no
  description is known to the fallback by its first sentence, each slot by
  its name ("how is the sport game going in city"), not its name: GLiNER
  scored "Game info" 0.27 for "how's the basketball game going in New
  Orleans?", too unsure to run it, and the sentence 0.96. Hints say it the
  same way.

## 0.2.0

- **Voice Labs is Voice Incubator.** As a Home Assistant app it is a new
  one (slug `voice_incubator`): what Voice Labs kept doesn't come along by
  itself. Everything new since Voice Labs is in the source's
  [changelog](https://github.com/OHF-Voice/voice-incubator/blob/v0.2.0/CHANGELOG.md#020).
