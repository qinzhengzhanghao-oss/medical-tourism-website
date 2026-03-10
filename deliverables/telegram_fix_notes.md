# Telegram continuity fix

## Goal
Make Telegram DM and WebChat share the same main session context as much as possible.

## Change applied
- Changed `~/.openclaw/openclaw.json`
- From: `session.dmScope = "per-channel-peer"`
- To: `session.dmScope = "main"`

## Reason
The prior setting isolated Telegram DM into its own session key (`agent:main:telegram:direct:<peer>`), which caused task/context split from WebChat.

## Expected result
- Telegram direct messages should route into the main session instead of a separate per-channel peer session.
- Cross-device continuity should improve.

## Follow-up
- Restart gateway/app runtime if required.
- Re-test by sending a Telegram DM and checking whether the active session remains `agent:main:main`.
