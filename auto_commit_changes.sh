#!/bin/bash
set -e

# --- CONFIGURATION ---
REPO_PATH=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_PATH")
MIRROR_PATH="${REPO_PATH}.git"
BFG_JAR="/opt/homebrew/Cellar/bfg/1.15.0/libexec/bfg-1.15.0.jar"  # Adjust if needed

cd "$REPO_PATH"
echo "🚀 Starting automatic commit + cleanup for $REPO_NAME..."

# --- FIND DELETED & ADDED FILES ---
deleted_files=$(git ls-files --deleted)
added_files=$(git ls-files --others --modified --exclude-standard)

echo
echo "📋 Changes detected:"
[ -n "$deleted_files" ] && echo "$deleted_files" | sed 's/^/  🗑️  /'
[ -n "$added_files" ] && echo "$added_files" | sed 's/^/  ➕  /'
echo

if [ -z "$deleted_files" ] && [ -z "$added_files" ]; then
  echo "⚠️  No changes to commit. Exiting."
  exit 0
fi

# --- ASK FOR COMMIT MESSAGE ---
read -p "✏️  Enter commit message: " commit_message

# --- COMMIT CHANGES ---
git add -A
git commit -m "$commit_message"
echo "✅ Commit created: '$commit_message'"

# --- CREATE MIRROR CLONE ---
cd "$(dirname "$REPO_PATH")"
rm -rf "$MIRROR_PATH"
git clone --mirror "$REPO_PATH" "$MIRROR_PATH"

# --- RUN BFG ON DELETED FILES ---
cd "$MIRROR_PATH"
if [ -n "$deleted_files" ]; then
  echo "🧹 Running BFG to remove deleted files from history..."
  java -jar "$BFG_JAR" --delete-files $deleted_files
else
  echo "✅ No deleted files to clean with BFG."
fi

# --- CLEAN GIT HISTORY ---
echo "🧽 Cleaning Git reflog and objects..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# --- PUSH CLEAN HISTORY ---
echo
read -p "📤 Push cleaned history to remote (force)? [y/N]: " confirm_push
if [[ "$confirm_push" =~ ^[Yy]$ ]]; then
  git push --force
  echo "✅ Force-pushed cleaned repo to remote."
else
  echo "🚫 Skipped remote push. Cleaned mirror remains at:"
  echo "   $MIRROR_PATH"
fi

echo
echo "🎯 All done! Repository cleaned and committed."