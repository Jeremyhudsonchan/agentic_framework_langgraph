# agentic_framework_langgraph

Agentic Framework with Langgraph and potentially Neo4j

## Agentic Framework

In workflow.ipynb, there is an example of layered tool calling. The example first calls the balance check tool, verifies if theres enough money in the database to make a transfer, then moves onto the next tool, funds transfer, which actually makes the transfer.

The expected behavior is that the balance check tool will return a boolean value, and the funds transfer tool will only be called if the balance check tool returns True. If the balance check tool returns False, the should continue function will inform the LLM that the workflow should not continue.