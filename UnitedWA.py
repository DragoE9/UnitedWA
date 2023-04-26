import nationstates
import csv
import Compliance_Evaluator as CompE
import datetime

user = input("Enter User Name: ")
api = nationstates.Nationstates(user + " Running UnitedWA.py by DragoE")
with open("regions.csv","r") as regions_file:
    reader = csv.reader(regions_file,delimiter=",")
    regions = [row for row in reader]
with open("recomendations.csv","r") as recs_file:
    reader2 = csv.reader(recs_file,delimiter=",")
    WA_recs = [row for row in reader2]
with open("votepower.csv","r") as power_file:
    reader3 = csv.reader(power_file,delimiter=",")
    Voting_Power = [row for row in reader3]

while True:
    user_select = input("Run a Command (type help for list): ").lower().strip()
    if user_select == "compliance":
        comp_report = []
        Chamber = input("GA or SC? ").upper().strip()
        if Chamber == "GA":
            for region in regions[0]:
                current_region = api.region(region)
                delegate = current_region.delegate
                nation = api.nation(delegate)
                vote = nation.gavote
                compliance = CompE.Compliance(WA_recs[0][0],vote)
                report_list = [region,delegate,vote,compliance]
                comp_report.append(report_list)
                print("{:20}  {:20}  {:8}  {:15}".format(region,delegate,vote,compliance))
        elif Chamber == "SC":
            for region in regions[0]:
                current_region = api.region(region)
                delegate = current_region.delegate
                nation = api.nation(delegate)
                vote = nation.scvote
                compliance = CompE.Compliance(WA_recs[0][1],vote)
                report_list = [region,delegate,vote,compliance]
                comp_report.append(report_list)
                print("{:20}  {:20}  {:8}  {:15}".format(region,delegate,vote,compliance))
        else:
            print("Unknown Chamber")
        if input("\nExport Report? ").lower().strip() == "yes":
            title = Chamber + " " + str(datetime.date.today()) + " Compliance Report.csv"
            with open(title,"w",newline="") as report_file:
                rep_writer = csv.writer(report_file,delimiter=",")
                rep_writer.writerows(comp_report)
    elif user_select == "power_refresh":
        print("\n")
        Voting_Power = []
        Power_Voting = []
        total_endo = 0
        total_member = 0
        total_power = 0
        WA_Nations = set(((api.wa(1).get_shards("members"))["members"]).split(","))
        for region in regions[0]:
            current_region = api.region(region)
            delegate = current_region.delegate
            nation = api.nation(delegate)
            del_endos = (nation.endorsements).split(",")
            num_endos = len(del_endos)
            members = set(((current_region.get_shards("nations"))["nations"]).split(":"))
            WA_members = WA_Nations.intersection(members)
            WA_number = len(WA_members)
            Power_Voting = [region,num_endos,WA_number,(num_endos+WA_number)]
            Voting_Power.append(Power_Voting)
            print("{:20}{:6}{:6}{:6}".format(region,num_endos,WA_number,Power_Voting[3]))
            total_endo += num_endos
            total_member += WA_number
            total_power += Power_Voting[3]
        Voting_Power.append(["TOTAL",total_endo,total_member,total_power])
        print("\n{} total voting power from {} delegate votes and {} individuals".format(total_power,total_endo,total_member))
        with open("votepower.csv","w",newline="") as power_file:
            writer = csv.writer(power_file,delimiter=",")
            writer.writerows(Voting_Power)
        print("Opperation Completed and File Saved\n")
    elif user_select == "rec_update":
        Chamber = input("GA or SC? ").upper().strip()
        New_rec = input("Set Reccomendation(FOR/AGAINST/NONE): ").upper().strip()
        if Chamber == "GA":
            WA_recs[0][0] = New_rec
        elif Chamber == "SC":
            WA_recs[0][1] = New_rec
        else:
            print("Unknown Chamber")
        with open ("recomendations.csv","w") as recs_file:
            writer2 = csv.writer(recs_file,delimiter=",")
            writer2.writerow(WA_recs[0])
    elif user_select == "region_add":
        new_entry = input("Enter a region: ").lower().strip()
        new_entry = new_entry.replace(" ","_")
        regions[0].append(new_entry)
        with open("regions.csv","w",newline="") as regions_file:
            writer = csv.writer(regions_file,delimiter=",")
            writer.writerow(regions[0])
    elif user_select == "region_del":
        to_remove = input("Enter a region: ").lower().strip()
        to_remove = to_remove.replace(" ","_")
        if to_remove in regions[0]:
            regions[0].remove(to_remove)
            with open("regions.csv","w",newline="") as regions_file:
                writer = csv.writer(regions_file,delimiter=",")
                writer.writerow(regions[0])
        else:
            print("No Such Region Found")
    elif user_select == "calc_vote":
        print("\nVotes are FOR,AGAINST,ABSTAIN,NONE")
        Rec = ""
        Bondage = "NON-BINDING"
        FOR = 0
        FOR_regions = []
        AGAINST = 0
        AGAINST_regions = []
        ABSTAIN = 0
        ABSTAIN_regions = []
        NONE_Vote = 0
        Non_voters = []
        for row in Voting_Power[0:-1]:
            printy_text = row[0] + " vote: "
            vote = input(printy_text).upper().strip()
            if vote == "FOR":
                FOR += int(row[3])
                FOR_regions.append(row[0])
            elif vote == "AGAINST":
                AGAINST += int(row[3])
                AGAINST_regions.append(row[0])
            elif vote == "ABSTAIN":
                ABSTAIN += int(row[3])
                ABSTAIN_regions.append(row[0])
            else:
                NONE_Vote += int(row[3])
                Non_voters.append(row[0])
        For_percent = CompE.VotePercenter(FOR,Voting_Power)
        Against_percent = CompE.VotePercenter(AGAINST,Voting_Power)
        Abstain_percent = CompE.VotePercenter(ABSTAIN,Voting_Power)
        Absent_percent = CompE.VotePercenter(NONE_Vote,Voting_Power)
        if FOR > AGAINST and FOR > ABSTAIN:
            Rec = "FOR"
            if For_percent >= 50:
                Bondage = "BINDING"
        elif AGAINST > ABSTAIN:
            Rec = "AGAINST"
            if Against_percent >= 50:
                Bondage = "BINDING"
        else:
            Rec = "NO RECOMENDATION"
        print("\n{} vote {}, with {} FOR, {} AGAINST, {} ABSTAIN, and {} ({} members) absent".format(Bondage,Rec,For_percent,Against_percent,Abstain_percent,Absent_percent,len(Non_voters)))
        if input("Export a vote report? ").lower().strip() == "yes":
            the_now = datetime.datetime.now()
            title = str(the_now.year) + str(the_now.month) + str(the_now.day) + str(the_now.hour) + str(the_now.minute) + " Vote Report.csv"
            for_list = ["FOR",FOR,For_percent] + FOR_regions
            ag_list = ["AGAINST",AGAINST,Against_percent] + AGAINST_regions
            abs_list = ["ABSTAIN",ABSTAIN,Abstain_percent] + ABSTAIN_regions
            No_list = ["No Vote",NONE_Vote,Absent_percent] + Non_voters
            export_list = [(for_list),(ag_list),(abs_list),(No_list)]
            with open(title,"w",newline="") as report_file:
                rep_writer = csv.writer(report_file,delimiter=",")
                rep_writer.writerows(export_list)
    elif user_select == "region_list":
        print("\n")
        for region in regions[0]:
            print(region)
        print("\n")
    elif user_select == "exit":
        break
    elif user_select == "help":
        print("\nAvailable Commands:\ncompliance - check compliance of dossier regions\nregion_add - add a region to the observance dossier\nregion_del - remove region from dossier\nregion_list - Lists all regions currently under observance\nrec_update - update voting recomendations\npower_refresh - update regional voting powers (DO NOT OVERUSE)\ncalc_vote - calculate WA vote recomendation based on URA standard formula\nexit - exit\n")
    else:
        print("Unknown Command")


