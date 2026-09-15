This module lets you prioritise business requirements with the RICE scoring
model, which is useful when you collect more requests than you can work on and
need to decide which ones to address first.

The score combines four estimates:

- **Reach**: how many users or events are affected over a given period.
- **Impact**: how much each affected user benefits, from minimal to massive.
- **Confidence**: how sure you are about your reach and impact estimates.
- **Effort**: the total work needed, usually in person-months.

They are combined as `Reach x Impact x Confidence / Effort`, so a requirement
that reaches many users for little work ranks above one that reaches few for a
lot of work. The resulting score is stored, which means you can sort and group
your requirements by it.

The priority field of the requirement is left untouched, so you can keep using
it alongside the score.
