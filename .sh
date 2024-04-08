#!/bin/bash
clear

tmux kill-session -t myapp

tmux new-session -d -s myapp
tmux split-window -h
tmux resize-pane -t 0 -x +10
tmux split-window -t 0 -v

tmux send-keys -t 1 'cd Backend' C-m
tmux send-keys -t 0 'cd Frontend' C-m

echo -e "\n"
echo -e "\t Checking if the environment exist"

if [ -d "./Backend/.env" ]; then
  echo -e "\t ✔️ Environment already exist !"
else
  echo -e "\t ❌ Environment does not exist exist !"
  echo -e "\t ⌛ Creating a new environment !"
  tmux send-keys -t 1 'python3 -m venv .env' C-m
  echo -e "\n"
fi

tmux send-keys -t 1 'source .env/bin/activate' C-m

tmux send-keys -t 2 'source Backend/.env/bin/activate' C-m


echo -e "\t ⌛ Installing all the dependencies!"
echo -e "------------------------------------------------------------------"
echo -e "\n\n"
cat Backend/requirements.txt
echo -e "------------------------------------------------------------------"
echo -e "\n\n"

tmux send-keys -t 1 'pip install -r requirements.txt' C-m

echo -e "\t ✔️ Installed all required dependencies! "

echo -e "\t ❓ Would you like to run all the servers in tmux window ? (y/n)"
read res

if [ "$res" == "y" ]; then
  echo -e "\n"

  echo -e "\t 🎉 Starting Flask App"
  tmux send-keys -t 1 'flask run --debug' C-m
  tmux send-keys -t 1 C-m C-m C-m C-m C-m C-m

  echo -e "\t 🎉 Starting Vue App"
  tmux send-keys -t 0 'npm run dev --host' C-m
  tmux send-keys -t 0 C-m C-m C-m C-m C-m C-m

  tmux send-keys -t 2 '(code .)' C-m
  tmux send-keys -t 2 'clear'

  tmux select-pane -t 2
  sleep 2
  tmux send-keys -t 2 C-m
  
  tmux attach-session -t myapp
else
  tmux kill-session -t myapp
fi
