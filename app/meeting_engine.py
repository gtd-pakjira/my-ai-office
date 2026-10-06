from agent import Agent
from models import MeetingRound
from hat_controller import ThinkingHat


class MeetingEngine:

    def __init__(
        self,
        team_lead: Agent,
        agents: dict[str, Agent],
    ):
        self.team_lead = team_lead
        self.agents = agents

    def run_round(self, session):

        print("\n" + "=" * 60)
        print(
            f"ROUND {len(session.rounds) + 1}"
        )
        print(
            f"HAT: {session.current_hat}"
        )
        print("=" * 60)

        available_agents = [
            name
            for name in self.agents
            if name != self.team_lead.name
        ]

        plan = self.team_lead.plan_round(
            session,
            available_agents,
        )

        print(
            f"\nObjective: {plan.objective}"
        )

        # --------------------------------------------------
        # Build task
        # --------------------------------------------------

        assignments = {
            assignment.agent: assignment
            for assignment in plan.assignments
            if assignment.agent in self.agents
            and assignment.agent != self.team_lead.name
        }

        # --------------------------------------------------
        # FORCE ANALYST PAIR
        # --------------------------------------------------

        if (
            "AI-2" in self.agents
            and "AI-3" in self.agents
        ):

            analyst_task = None

            if "AI-2" in assignments:
                analyst_task = assignments[
                    "AI-2"
                ].task

            elif "AI-3" in assignments:
                analyst_task = assignments[
                    "AI-3"
                ].task

            if analyst_task:

                assignments["AI-2"] = type(
                    assignments.get("AI-2")
                    or assignments["AI-3"]
                )(
                    agent="AI-2",
                    task=analyst_task,
                )

                assignments["AI-3"] = type(
                    assignments.get("AI-3")
                    or assignments["AI-2"]
                )(
                    agent="AI-3",
                    task=analyst_task,
                )

        print("\nAssignments:")

        for assignment in assignments.values():
            print(
                f"- {assignment.agent}: "
                f"{assignment.task}"
            )

        meeting_round = MeetingRound(
            hat=session.current_hat,
            objective=plan.objective,
            assignments=list(
                assignments.values()
            ),
        )

        session.rounds.append(
            meeting_round
        )

        # --------------------------------------------------
        # AI-2 + AI-3
        # Independent analysis
        # --------------------------------------------------

        analyst_results = []

        for agent_name in [
            "AI-2",
            "AI-3",
        ]:

            assignment = assignments.get(
                agent_name
            )

            if not assignment:
                continue

            agent = self.agents[
                agent_name
            ]

            print(
                f"\n[{agent.name}] "
                f"Independent Analysis..."
            )

            result = agent.execute_assignment(
                session,
                assignment,
            )

            analyst_results.append(result)

            meeting_round.results.append(
                result
            )

            print(
                f"[{agent.name}] Done"
            )

            print(result.response)

        # --------------------------------------------------
        # Context from Analyst results
        # --------------------------------------------------

        analyst_context = "\n\n".join(
            f"[{result.agent}]\n"
            f"{result.response}"
            for result in analyst_results
        )

        # --------------------------------------------------
        # AI-4 REVIEWER
        # --------------------------------------------------

        reviewer = self.agents.get("AI-4")

        if reviewer:

            assignment = assignments.get(
                "AI-4"
            )

            if not assignment:

                assignment = type(
                    list(assignments.values())[0]
                )(
                    agent="AI-4",
                    task=(
                        "ตรวจสอบผลการวิเคราะห์ "
                        "ของ AI-2 และ AI-3 "
                        "หาข้อมูลที่ตรงกัน "
                        "ข้อมูลที่ขัดแย้ง "
                        "และข้อมูลที่ยังขาด"
                    ),
                )

            print(
                "\n[AI-4] Reviewing..."
            )

            result = reviewer.execute_assignment(
                session,
                assignment,
                context=analyst_context,
            )

            meeting_round.results.append(
                result
            )

            print(
                "[AI-4] Done"
            )

            print(result.response)

            reviewer_context = (
                analyst_context
                + "\n\n[AI-4]\n"
                + result.response
            )

        else:

            reviewer_context = analyst_context

        # --------------------------------------------------
        # AI-5 CHALLENGER
        # --------------------------------------------------

        challenger = self.agents.get(
            "AI-5"
        )

        if challenger:

            assignment = assignments.get(
                "AI-5"
            )

            if not assignment:

                assignment = type(
                    list(assignments.values())[0]
                )(
                    agent="AI-5",
                    task=(
                        "ท้าทายผลการวิเคราะห์ "
                        "ค้นหา assumptions "
                        "จุดอ่อน "
                        "และข้อสรุปที่อาจผิด"
                    ),
                )

            print(
                "\n[AI-5] Challenging..."
            )

            result = challenger.execute_assignment(
                session,
                assignment,
                context=reviewer_context,
            )

            meeting_round.results.append(
                result
            )

            print(
                "[AI-5] Done"
            )

            print(result.response)

            challenger_context = (
                reviewer_context
                + "\n\n[AI-5]\n"
                + result.response
            )

        else:

            challenger_context = (
                reviewer_context
            )

        # --------------------------------------------------
        # AI-6 WILD CARD
        # --------------------------------------------------

        wild_card = self.agents.get(
            "AI-6"
        )

        if wild_card:

            assignment = assignments.get(
                "AI-6"
            )

            if not assignment:

                assignment = type(
                    list(assignments.values())[0]
                )(
                    agent="AI-6",
                    task=(
                        "มองหาแง่มุมที่ทีมยังไม่ได้ "
                        "พิจารณา "
                        "และระบุ blind spots "
                        "ที่อาจส่งผลต่อเป้าหมาย"
                    ),
                )

            print(
                "\n[AI-6] Wild Card Analysis..."
            )

            result = wild_card.execute_assignment(
                session,
                assignment,
                context=challenger_context,
            )

            meeting_round.results.append(
                result
            )

            print(
                "[AI-6] Done"
            )

            print(result.response)

        return meeting_round

    def move_next(
        self,
        session,
    ):

        decision = (
            self.team_lead
            .decide_hat_direction(session)
        )

        print(
            "\n--- AI-1 Hat Decision ---"
        )

        print(
            f"Direction: "
            f"{decision.direction}"
        )

        print(
            f"Reason: "
            f"{decision.reason}"
        )

        current_index = (
            self.team_lead
            .hat_controller
            .current_index
        )

        if decision.direction == "FORWARD":

            if current_index >= 5:
                return False

            self.team_lead.move_forward()

        elif decision.direction == "BACKWARD":

            if current_index <= 0:

                print(
                    "Already at WHITE. "
                    "Cannot move backward."
                )

                return False

            self.team_lead.move_backward()

        else:

            print(
                f"Invalid direction: "
                f"{decision.direction}"
            )

            return False

        session.current_hat = (
            self.team_lead
            .hat_controller
            .current_hat
            .value
        )

        print(
            f"\nNext Hat: "
            f"{session.current_hat}"
        )

        return True

    def run(
        self,
        session,
        max_rounds: int = 12,
    ):

        while (
            session.current_hat
            != ThinkingHat.BLUE.value
            and
            len(session.rounds)
            < max_rounds
        ):

            self.run_round(
                session
            )

            if not self.move_next(
                session
            ):
                break

        if (
            session.current_hat
            == ThinkingHat.BLUE.value
        ):

            self.run_round(
                session
            )

            print(
                "\n--- Creating Final Proposal ---"
            )

            proposal = (
                self.team_lead
                .create_final_proposal(
                    session
                )
            )

            session.final_proposal = (
                proposal
            )

            session.status = (
                "COMPLETED"
            )

        else:

            session.status = (
                "STOPPED"
            )

        return session