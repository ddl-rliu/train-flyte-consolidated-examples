TFCE_WORKFLOWS="./train-flyte-consolidated-examples/workflows"
TFCE_RUN="pyflyte run --remote"
$TFCE_RUN $TFCE_WORKFLOWS/art-test.py wf
$TFCE_RUN $TFCE_WORKFLOWS/art-test2.py wf
$TFCE_RUN $TFCE_WORKFLOWS/art-workflows.py wf
$TFCE_RUN $TFCE_WORKFLOWS/artifacts.py wf
$TFCE_RUN $TFCE_WORKFLOWS/flow.py wf
$TFCE_RUN $TFCE_WORKFLOWS/inputs_rare_workflow.py wf
$TFCE_RUN $TFCE_WORKFLOWS/inputs_workflow.py wf
$TFCE_RUN $TFCE_WORKFLOWS/nested_workflow.py wf
$TFCE_RUN $TFCE_WORKFLOWS/unions_workflow.py wf