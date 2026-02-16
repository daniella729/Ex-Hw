from soultion.git_command import git_command_simulator
def test_check_add()->None:
    commend= "git add hw1.py"
    assert git_command_simulator(commend)=="stage specific file hw1.py for the next commit."
def test_check_rm()->None:
    commend="git rm --cached hw1.py"
    assert git_command_simulator(commend)=="Unstage file hw1.py while retaining the changes in the working directory."

def test_empty_command()->None:
    commend=""
    assert git_command_simulator(commend)=="Invalid git command."

def test_incomeplte_command()->None:
    commend="git add" 
    assert git_command_simulator(commend)=="Invalid git command."

def test_incomplete_rm_commend()->None:
    commend="git rm --cached" 
    assert git_command_simulator(commend)=="Invalid git command."   

def test_command_stash()->None:
    commend="git stash apply"
    assert git_command_simulator(commend)=="Applies the most recently stashed changes."
    commend="git stash push -m fix ex1"
    assert git_command_simulator(commend)=="Stashes changes with a custom message fix ex1 for easy identification."
    commend="git stash apply hw1"
    assert git_command_simulator(commend)=="Applies the stashed changes with the specified name hw1."
