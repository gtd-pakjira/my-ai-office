from agent import Agent, AgentRole
from meeting_engine import MeetingEngine


team_lead = Agent(
    name="AI-1",
    role=AgentRole.TEAM_LEAD,
)

analyst_2 = Agent(
    name="AI-2",
    role=AgentRole.ANALYST,
)

analyst_3 = Agent(
    name="AI-3",
    role=AgentRole.ANALYST,
)

reviewer_4 = Agent(
    name="AI-4",
    role=AgentRole.REVIEWER,
)

challenger_5 = Agent(
    name="AI-5",
    role=AgentRole.CHALLENGER,
)

wild_card_6 = Agent(
    name="AI-6",
    role=AgentRole.WILD_CARD,
)


session = team_lead.start_meeting(
    "เรากำลังจะสร้างระบบลาออนไลน์สำหรับบริษัทเล็ก ๆ"
)


agents = {
    analyst_2.name: analyst_2,
    analyst_3.name: analyst_3,
    reviewer_4.name: reviewer_4,
    challenger_5.name: challenger_5,
    wild_card_6.name: wild_card_6,
}


engine = MeetingEngine(
    team_lead=team_lead,
    agents=agents,
)


print("AI OFFICE")
print("=" * 60)
print(f"Goal: {session.goal}")
print(f"Team Lead: {team_lead.name}")
print(
    f"Agents: {', '.join(agents.keys())}"
)


session = engine.run(session)


print("\n")
print("=" * 60)
print("MEETING COMPLETE")
print("=" * 60)

print(
    f"\nStatus: {session.status}"
)

print(
    f"Rounds: {len(session.rounds)}"
)

print(
    f"Final Hat: {session.current_hat}"
)


if session.final_proposal:

    print(
        "\n--- FINAL SUMMARY ---"
    )

    print(
        session.final_proposal.summary
    )

    print(
        "\n--- FINAL PROPOSAL ---"
    )

    print(
        session.final_proposal.proposal
    )