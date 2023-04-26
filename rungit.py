from github import Github

# using an access token
g = Github("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")

def append_this(email,pass1):
	repo = g.get_user().get_repo("maituliao")
	paper = repo.get_contents("/acctcreated.csv")
	existing = paper.decoded_content.decode()
	new_data = f"\n{email},{pass1}"
	repo.update_file("acctcreated.csv", "created new account", f"{existing}{new_data}", paper.sha)