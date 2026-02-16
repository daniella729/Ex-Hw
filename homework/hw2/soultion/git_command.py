INVALID_COMMAND = "Invalid git command."


def check_input_user(git_command: str) -> list[str] | str:
    """Validate basic git command structure and return parsed command or error message."""
    command = git_command.split()
    if command:
        if command[0] == "git":
            if len(command) >= 2:
                return command

    return INVALID_COMMAND


def git_command_simulator(git_command: str) -> str:
    """Simulate git commands and return a description of the requested action."""
    command = check_input_user(git_command)
    if isinstance(command, str):
        return command
    result: str

    match (command[1]):
        case "add":
            result = git_add_command(command)
        case "rm":
            result = check_rm_case(command)
        case "commit":
            result = check_commit_case(command)
        case "push":
            result = "Upload your commits to the remote repository."
        case "stash":
            result = check_stash_case(command)
        case _:
            result = "Unknown git command."
    return result


def git_add_command(add_command: list[str]) -> str:
    """Handle git add command and return the appropriate action message."""
    if len(add_command) < 3:
        return INVALID_COMMAND
    elif add_command[2] == ".":
        return "stage all changes"
    else:
        return f"stage specific file {add_command[2]} for the next commit."


def check_commit_case(command_commit: list[str]) -> str:
    """Handle git commit command variations."""
    if len(command_commit) < 4 or command_commit[2] != "-m":
        return INVALID_COMMAND
    message = " ".join(command_commit[3:])
    return f"Commit changes to the repository with a descriptive message {message}."


def check_rm_case(command_rm: list[str]) -> str:
    """Handle git rm command variations."""
    if len(command_rm) < 4 or command_rm[2] != "--cached":
        return INVALID_COMMAND
    else:
        return f"Unstage file {command_rm[3]} while retaining the changes in the working directory."


def check_stash_case(command_stash: list[str]) -> str:
    """Handle git stash command variations."""
    if len(command_stash) == 2:
        return "Temporarily shelves changes in your working directory so you can work on a different task."
    elif command_stash[2] == "apply":
        return check_stash_apply(command_stash)
    elif command_stash[2] == "push":
        return check_stash_push(command_stash)
    else:
        return INVALID_COMMAND


def check_stash_apply(command_stash: list[str]) -> str:
    """Handle 'git stash apply' variations."""
    if len(command_stash) == 3:
        return "Applies the most recently stashed changes."
    if len(command_stash) == 4:
        return f"Applies the stashed changes with the specified name {command_stash[3]}."
    return INVALID_COMMAND


def check_stash_push(command_stash: list[str]) -> str:
    """Handle 'git stash push' variations."""
    if  len(command_stash)>=5 and command_stash[3] == "-m":
        message = " ".join(command_stash[4:])
        return (
            f"Stashes changes with a custom message {message} "
            "for easy identification."
        )
    return "Invalid stash command."


def main() -> None:
    """Run the git command simulator by reading user input and printing the result."""
    user_input = input("Enter command :")
    result = git_command_simulator(user_input)
    print(result)
