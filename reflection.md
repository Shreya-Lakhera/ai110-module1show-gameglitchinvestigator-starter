# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

I started by reviewing app.py and logic_utils.py. Testing the helper functions showed that the hints were backwards: a guess above the secret told the player to go higher. I also found that alternating attempts compared numbers as text, which could incorrectly label 9 as higher than 50. Reviewing the reset code showed that New Game did not clear the won or lost status, although I did not test that behavior in the browser. All four functions in logic_utils.py were unfinished and raised NotImplementedError when called.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

- The hints were backwards: guessing above the secret told the player to go higher, and guessing below it told them to go lower.
- On alternating attempts, numbers were compared as text, so a guess of 9 could incorrectly count as higher than a secret of 50.
- The New Game button did not reset the game’s status, leaving players unable to play again after winning or losing.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| `check_guess(60, 50)` | Identify the guess as too high and tell the player to go lower. | Correctly identified “Too High,” but instructed the player to go higher. | `('Too High', '📈 Go HIGHER!')` |
| `check_guess(40, 50)` | Identify the guess as too low and tell the player to go higher. | Correctly identified “Too Low,” but instructed the player to go lower. | `('Too Low', '📉 Go LOWER!')` |
| `check_guess(9, "50")` | Compare the numeric values and identify 9 as too low. | Compared strings and incorrectly identified 9 as too high. | `('Too High', '📈 Go HIGHER!')` |
| `logic_utils.check_guess(50, 50)` | Return a winning outcome and message. | Raised an error because the function was not implemented. | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
