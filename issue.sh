gh auth refresh -s project

OWNER=Ilaivdv       
NUM=1   #project number                                 
REPO=Ilaivdv/codam-pacman 
N=103         #issuename, this is a test issue                           

PID=$(gh project view $NUM --owner $OWNER --format json --jq .id)
FIELDS=$(gh project field-list $NUM --owner $OWNER --format json)
START=$(echo "$FIELDS" | jq -r '.fields[]|select(.name=="Created").id')
END=$(echo "$FIELDS" | jq -r '.fields[]|select(.name=="Closed").id')

echo "PID=$PID"
echo "START=$START"
echo "END=$END"

ITEM=$(gh project item-list $NUM --owner $OWNER -L 200 --format json \
  | jq -r ".items[] | select(.content.number==$N) | .id")

S=$(gh issue view $N -R $REPO --json createdAt --jq '.createdAt[:10]')
E=$(gh issue view $N -R $REPO --json closedAt --jq '(.closedAt // "")[:10]')

echo "ITEM=$ITEM  START_DATE=$S  END_DATE=$E"

gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$START" --date "$S"
[ -n "$E" ] && gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$END" --date "$E"