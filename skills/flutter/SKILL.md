---
name: flutter
description: How we build, analyze, test and release Flutter and Dart apps, covering project structure, state management with Riverpod or Bloc, routing with go_router, code generation, flavors and environment config, Firebase and Supabase integration, and store release checks. Use whenever working in a Flutter or Dart codebase, writing widgets, state or navigation, fixing analyzer warnings, running build_runner, upgrading Flutter or packages, preparing an Android or iOS release, or when you see pubspec.yaml, analysis_options.yaml or lib/main.dart.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, flutter, dart, mobile]
---

# Flutter

Layered apps (UI → state → data), one state-management approach per app,
and the analyzer kept at zero warnings.

## Before you start

1. Check the Flutter version: `.fvmrc` / `.fvm/` (use `fvm flutter ...`
   if present), the `environment:` block in `pubspec.yaml`, and CI. Don't
   upgrade Flutter as a side effect of another task.
2. Identify the state-management and routing libraries already in use
   (Riverpod, Bloc, Provider, GetX; go_router, auto_route) and follow them.
   Two state approaches in one app is a maintenance tax.
3. Read `analysis_options.yaml` for the lint set (`flutter_lints`,
   `very_good_analysis`, custom).

## Defaults for new projects

- Latest stable Flutter (3.47 / Dart 3.13 today), pinned with FVM.
- Structure by feature: `lib/features/<feature>/{data,domain,presentation}`,
  with shared code in `lib/core/`.
- State: Riverpod 3 (`flutter_riverpod`) or Bloc 9; routing: `go_router`.
- Models: `freezed` + `json_serializable` via `build_runner`.
- Lints: `very_good_analysis` (strict) or `flutter_lints` (lighter).
- Environments via flavors plus `--dart-define-from-file=env/dev.json`.

## Verify loop

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs   # if codegen is used
dart format --set-exit-if-changed .
flutter analyze                     # zero issues, not just zero errors
flutter test
flutter build appbundle --flavor prod   # / flutter build ipa, before release work
```

## Rules that matter

- **Keep `build()` pure and cheap:** no I/O, no object creation that should
  live in state; use `const` constructors wherever possible.
- **After `await`, check `context.mounted`** before using `BuildContext`
  (navigation, snackbars).
- **Dispose what you create:** controllers, streams, focus nodes, timers.
  Prefer `autoDispose` providers / Bloc lifecycles.
- **Data layer owns I/O:** repositories wrap HTTP (`dio`), Firebase or
  Supabase; widgets never call them directly.
- **No secrets in the app binary.** Anything in Dart code or
  `--dart-define` can be extracted. Use backend-issued tokens; Firebase and
  Supabase client keys are public by design and must be protected by rules
  or RLS.
- **Generated files:** follow the repo convention for committing or
  ignoring `*.g.dart` / `*.freezed.dart`, and regenerate after model edits.
- **Platform setup:** Firebase via `flutterfire configure` per flavor;
  Supabase via `supabase_flutter` with the publishable key.

## Changed recently (checked 2026-10-23)

- Current stable: **Flutter 3.47.7 / Dart 3.13.5**. Current package majors:
  `flutter_riverpod` 3, `flutter_bloc` 9, `go_router` 18, `freezed` 4,
  `firebase_core` 5, `cloud_firestore` 7, `supabase_flutter` 2.
- Major bumps (Riverpod 2→3, freezed 2/3→4, go_router) change APIs; upgrade
  one package per PR and read its changelog/migration guide.
- **Store requirements move yearly** (Google Play target API level, App
  Store minimum Xcode/SDK). Check both before a release branch is cut.

## Pitfalls

- `setState` after dispose, from async callbacks without a mounted check.
- Huge widget files mixing layout, state and data calls; split by layer.
- Platform folders (`android/`, `ios/`) edited without updating flavor
  configs for every flavor.
- Testing only on one platform or screen size; run at least one Android and
  one iOS build before release.

## Sources

- `research/2026-10-23-stack-baseline.md` → Flutter section.
