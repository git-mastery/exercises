#!/bin/bash

echo "Do you want to create a hands-on or an exercise? (hands-on/exercise, h/e)"
read choice

case "$choice" in
"hands-on" | "h" | "H")
  python new-hands-on.py
  ;;
"exercise" | "e" | "E")
  python new-exercise.py
  ;;
*)
  echo "Invalid choice. Please enter 'hands-on' (h) or 'exercise' (e)."
  ;;
esac
