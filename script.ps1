# Set the target date for all commits
$targetDate = Get-Date "2025-07-07T10:00:00"
$formattedDate = $targetDate.ToString("yyyy-MM-ddTHH:mm:ss")

# Set your source and destination branches
$sourceBranch = "main" # change as needed
$newBranch = "rewritten-history"

# Start from detached HEAD to avoid affecting current branch
git switch --detach

# Create a new orphan branch
git checkout --orphan $newBranch
git reset --hard

# Make an initial empty commit
git commit --allow-empty -m "Start of rewritten history"

# Get commits from source branch (oldest to newest)
$commits = git rev-list --reverse $sourceBranch

foreach ($commit in $commits) {
    # Get commit metadata
    $authorName = git log -1 --format="%an" $commit
    $authorEmail = git log -1 --format="%ae" $commit
    $message = git log -1 --format="%B" $commit

    # Read commit contents into the index
    git read-tree --reset -u $commit

    # Stage all files
    git add -A

    # Set fixed commit dates
    $env:GIT_AUTHOR_DATE = $formattedDate
    $env:GIT_COMMITTER_DATE = $formattedDate

    # Commit with preserved author and message
    git commit --author="$authorName <$authorEmail>" -m "$message"
}

# Clean up environment variables
Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE

Write-Host "`n✅ All commits have been rewritten with the date $formattedDate in branch '$newBranch'."
