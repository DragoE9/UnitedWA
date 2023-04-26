def Compliance(Rec,vote):
    """Takes in a recomendation and a vote, evaluates compliance. Returns a string"""
    if (vote == Rec) or (Rec == "NONE"):
        return "Compliant"
    elif vote == "None":
        return "No Vote"
    else:
        return "Non-Compliant"
def VotePercenter(Votes,Voting_Power):
    return round(((float(Votes)/float(Voting_Power[-1][3]))*100),2)
