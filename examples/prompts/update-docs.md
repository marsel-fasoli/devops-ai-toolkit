# @update-docs

Run this at the end of every session to keep the knowledge base fresh.

## Steps

1. **Review this session's work**
   - What new information did we discover?
   - What did we try that didn't work? (equally important to document)
   - Did any existing documentation turn out to be wrong or stale?
   - Did the AI have to ask about something it should have known?

2. **Update product.md**
   - Add any new facts, paths, versions, or conventions discovered this session
   - Fix any information that turned out to be wrong
   - Update ticket statuses if anything changed
   - If the AI had to ask about something twice — it belongs in product.md

3. **Update or create documentation files**
   - If a topic grew too large in product.md — split it into its own file in docs/
   - If a new area was investigated — create a new doc file for it
   - If an existing doc file is now outdated — fix it

4. **Update ticket folders**
   - If we worked on a specific issue — update the investigation notes in its folder
   - Add any new screenshots or log files captured this session
   - If an issue was resolved — mark it closed in product.md and write the final root cause in the ticket folder

5. **Check for new prompts**
   - Did we repeat a multi-step workflow more than twice this session?
   - If yes — should it become a new prompt?
   - Suggest the prompt name and what it should do

6. **Check for system improvements**
   - Review any "💡 System improvement idea" flags from this session
   - Decide which ones to act on now vs later
   - If acting now — make the change
   - If later — note it somewhere visible

7. **Confirm everything is saved**
   - All new files created
   - All edited files saved
   - Backup will run automatically on schedule (or run manually if something important was added)

## Output

At the end, give a short summary:
- What was updated
- What new prompts were proposed (if any)
- What system improvements were flagged (if any)
- Any open questions for next session
