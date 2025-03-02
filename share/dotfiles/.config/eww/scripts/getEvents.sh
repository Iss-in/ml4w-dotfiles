#!/bin/bash

#!/bin/bash

width=30
getCurrentTitle() {
  text=$(jq -r '.["0"].title // empty' /tmp/events.json  |  fold -w $width | sed 's/^[[:space:]]*//' )
  echo "$text"
}

getCurrentInterval(){
  start=$(jq -r '.["0"].start // empty' /tmp/events.json || echo "")
  end=$(jq -r '.["0"].end // empty' /tmp/events.json || echo "")
  echo $start-$end
}

getNextTitle() {
  text=$(jq -r '.["1"].title // empty' /tmp/events.json  |  fold -w $width | sed 's/^[[:space:]]*//' )
  echo "$text"
}

getNextInterval() {
  start=$(jq -r '.["1"].start // empty' /tmp/events.json || echo "")
  end=$(jq -r '.["1"].end // empty' /tmp/events.json || echo "")
  echo $start-$end
}

getUpcomingTime() {
  upcoming_time=$(jq -r '.["1"].start // empty' /tmp/events.json  | sed 's| .*||')
  target_time=$(date -d "$upcoming_time" +%H:%M)
  current_time=$(date +%H:%M)
  diff_seconds=$(( $(date -d "$target_time" +%s) - $(date -d "$current_time" +%s) ))
  # Convert seconds to hours and minutes
  hours=$(( diff_seconds / 3600 ))
  minutes=$(( (diff_seconds % 3600) / 60 ))

  # Display the result
  if [[ -n $upcoming_time ]];then
    echo "  ${hours}h${minutes}m"
  fi

}

# getNextTitle() {
#   jq -r '.["1"].title' /tmp/events.json 
# }

# getNextInterval() {
#   jq -r '.["1"].interval' /tmp/events.json 
# }

updateAll(){
  # echo 1 >> /home/kushy/test.txt
  # notify-send running now
  
  eww update tasks-json="$(cat /tmp/events.json)"
  echo "hehe"
}


verbose='false'
while getopts 'abcduzv' flag; do
  case "${flag}" in
    a) getCurrentTitle;;
    b) getCurrentInterval;;
    c) getNextTitle;;
    d) getNextInterval;;
    u) getUpcomingTime;;
    z) updateAll;;

    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done


