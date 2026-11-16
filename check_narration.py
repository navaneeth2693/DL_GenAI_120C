from narrator import narrate

outcome = (
    "You do not have the brass key. "
    "Find and collect it before using it."
)

print("Requesting narration...", flush=True)

reply, source = narrate(outcome)

print("Source:", source)
print("Reply:", reply)

assert outcome in reply
print("The Python-approved outcome was preserved.")