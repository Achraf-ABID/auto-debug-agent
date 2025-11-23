# Bug Hunter Agent Fixes

## Current Status
The agent runs but fails to fix bugs in `examples/buggy_math.py`. Console output is truncated.

## Todo
- [/] Fix truncated console output (Rich configuration) <!-- id: 0 -->
- [/] Improve logging to capture sandbox output <!-- id: 1 -->
- [/] Investigate why `gemini-2.5-flash` fails to fix the code <!-- id: 2 -->
- [/] Tune LLM prompts if necessary <!-- id: 3 -->
- [ ] Implement Multi-Agent System <!-- id: 5 -->
    - [x] Create `src/agents/` directory and `base_agent.py` <!-- id: 6 -->
    - [x] Implement `QAAgent` <!-- id: 7 -->
    - [x] Implement `DevAgent` <!-- id: 8 -->
    - [x] Implement `ManagerAgent` <!-- id: 9 -->
    - [x] Update `main.py` to use `ManagerAgent` <!-- id: 10 -->
    - [/] Verify MAS workflow <!-- id: 11 -->
