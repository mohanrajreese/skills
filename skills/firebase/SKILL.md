---
name: firebase
description: How we build on Firebase, covering Firestore data modeling and security rules, Auth, Cloud Functions 2nd gen, the Emulator Suite, App Check, Hosting and App Hosting, multi-environment projects, and current deprecations such as the Dynamic Links shutdown and the Extensions sunset. Use whenever working with Firebase in web, Node or Flutter apps, writing or reviewing firestore.rules or storage.rules, designing Firestore collections and indexes, writing Cloud Functions, configuring firebase.json, deploying with firebase-tools, or when you see .firebaserc, firebase.json or a FlutterFire config.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, firebase, gcp, backend, mobile]
---

# Firebase

In Firebase apps the client talks straight to the database, so **security
rules are the backend's authorization layer.** Most Firebase incidents are
open or wrong rules.

## Before you start

1. Read `.firebaserc` (project aliases) and `firebase.json` (which products
   and emulators are configured). Run `firebase use` to see the active
   project, and say which project you're about to deploy to.
2. Read `firestore.rules`, `storage.rules` and `firestore.indexes.json`
   before changing any data access.
3. Check SDK versions: web modular SDK (`firebase` 13.x), `firebase-admin`,
   `firebase-functions`, or FlutterFire packages.

## Defaults for new work

- **Separate Firebase projects per environment** (dev / staging / prod) with
  aliases in `.firebaserc`. Never point development builds at prod.
- **Emulator Suite** for local dev and tests: `firebase emulators:start`,
  `firebase emulators:exec "npm test"` in CI.
- **Functions:** 2nd gen (`firebase-functions/v2/*` imports), TypeScript,
  region set explicitly, secrets via `defineSecret` (Secret Manager).
- **App Check** enforced on Firestore, Storage, Functions and callable
  endpoints for production apps.
- **Hosting** for static/SPA sites; **App Hosting** for SSR frameworks
  (Next.js, Angular) with GitHub-connected rollouts.

## Verify loop

```bash
firebase use                                   # right project?
firebase emulators:exec --only firestore,auth "npm test"   # rules + function tests
npm --prefix functions run build && npm --prefix functions run lint
firebase deploy --only firestore:rules --dry-run   # validate before a real deploy
firebase deploy --only functions:NAME          # deploy narrowly, not everything
```

## Rules that matter

- **Rules deny by default.** Every `allow` checks `request.auth`, ownership
  (`request.auth.uid == resource.data.ownerId`) and the shape of incoming
  data (`request.resource.data.keys().hasOnly([...])`, types, sizes).
  Never ship "test mode" rules (`allow read, write: if true` or a date
  check).
- **Test rules** with `@firebase/rules-unit-testing` against the emulator,
  covering at least: owner allowed, other user denied, unauthenticated
  denied, invalid fields denied.
- **Model Firestore around queries:** denormalise for reads, keep documents
  well under the 1 MiB limit, use subcollections for unbounded lists, and add
  composite indexes to `firestore.indexes.json` (commit them).
- **Costs scale with reads:** paginate with cursors (`startAfter`), avoid
  listeners on large collections, and don't fetch in loops.
- **Admin SDK** bypasses rules. Use it only on trusted servers/functions,
  with ADC credentials; never commit service-account JSON.
- The web `apiKey` in config is an identifier, not a secret. Restrict it in
  Google Cloud console and rely on rules plus App Check.

## Changed recently (checked 2026-10-23)

- **Dynamic Links shut down on 2025-08-25**; links stopped working. Use
  App Links / Universal Links or another deep-link service.
- **Firebase Extensions service shuts down on 2027-03-31.** Deployed
  extensions keep running but can't be updated or reconfigured through
  Firebase. Migrate to 2nd-gen functions now (firebase-tools 15.32+ has
  migration tooling).
- **1st-gen Functions are legacy** and tied to older Node runtimes; write new
  functions on 2nd gen and migrate old ones when you touch them.
- Current majors: `firebase` 13, `firebase-admin` 14, `firebase-functions`
  7, `firebase-tools` 15; FlutterFire `firebase_core` 5.

## Pitfalls

- Rules that check `resource.data` on create (it doesn't exist yet; use
  `request.resource.data`).
- Monotonically increasing document IDs or timestamps in indexed fields at
  high write rates, which create hotspots.
- Deploying all of `firebase deploy` from a laptop and overwriting rules or
  functions someone else changed.

## Sources

- `research/2026-10-23-stack-baseline.md` → Firebase section.
