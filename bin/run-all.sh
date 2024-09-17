TFCE_LOG="flyte-workflows.log"
echo "" > $TFCE_LOG

TFCE_WORKFLOWS="./train-flyte-consolidated-examples/workflows"
TFCE_RUN="pyflyte run --remote"
$TFCE_RUN $TFCE_WORKFLOWS/artifacts_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/caching_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/inputs_complex_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/inputs_rare_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/inputs_unions_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/nested_workflow.py wf &>> $TFCE_LOG