from enum import Enum

from ollama_client import chat
from models import (
    Assignment,
    AgentResult,
    FinalProposal,
    HatDecision,
    MeetingSession,
    RoundPlan,
)
from hat_controller import HatController


class AgentRole(str, Enum):
    TEAM_LEAD = "TEAM_LEAD"
    ANALYST = "ANALYST"
    REVIEWER = "REVIEWER"
    CHALLENGER = "CHALLENGER"
    WILD_CARD = "WILD_CARD"


HAT_GUIDANCE = {
    "WHITE": """
รวบรวมข้อเท็จจริง ข้อมูลที่มีอยู่ และข้อมูลที่ยังขาด
ห้ามเสนอ solution
ห้ามตัดสินว่าอะไรดีที่สุด
ห้ามสร้างข้อเท็จจริงที่ไม่มีข้อมูลรองรับ
""",

    "RED": """
สำรวจความรู้สึก ความกังวล สัญชาตญาณ และประสบการณ์ของผู้เกี่ยวข้อง
ไม่จำเป็นต้องพิสูจน์เหตุผลทุกข้อ
""",

    "BLACK": """
ค้นหาความเสี่ยง ปัญหา ข้อจำกัด จุดอ่อน และสิ่งที่อาจผิดพลาด
ต้องพยายามมองหาสิ่งที่ทีมอาจมองข้าม
""",

    "YELLOW": """
ค้นหาประโยชน์ คุณค่า โอกาส และผลลัพธ์เชิงบวกที่เป็นไปได้
""",

    "GREEN": """
เสนอแนวทางใหม่ ทางเลือก และความคิดสร้างสรรค์
สามารถท้าทายสมมติฐานเดิมได้
""",

    "BLUE": """
จัดระเบียบสิ่งที่ทีมค้นพบ
สรุปประเด็น
ระบุสิ่งที่ตัดสินใจได้
ระบุสิ่งที่ยังไม่แน่นอน
และเตรียมข้อเสนอสุดท้าย
""",
}


class Agent:

    def __init__(
        self,
        name: str,
        role: AgentRole,
    ):
        self.name = name
        self.role = role
        self.hat_controller = HatController()

    def start_meeting(
        self,
        task: str,
    ) -> MeetingSession:

        return MeetingSession(
            goal=task,
            current_hat=self.hat_controller.current_hat.value,
            status="ACTIVE",
        )

    def plan_round(
        self,
        session: MeetingSession,
        available_agents: list[str],
    ) -> RoundPlan:

        hat = session.current_hat

        prompt = f"""
/no_think

คุณกำลังทำหน้าที่เป็น TEAM LEAD ของ AI Office

เป้าหมายการประชุม:
{session.goal}

Thinking Hat ปัจจุบัน:
{hat}

กติกาของ Hat นี้:
{HAT_GUIDANCE[hat]}

Agent ที่สามารถมอบหมายงานได้:
{", ".join(available_agents)}

หน้าที่:
วางแผนการทำงานของรอบปัจจุบัน

กฎสำคัญ:
- ห้ามมอบหมายงานให้ TEAM LEAD
- ใช้เฉพาะ Agent ที่อยู่ในรายชื่อที่กำหนด
- งานต้องสอดคล้องกับ Hat ปัจจุบัน
- งานต้องเกี่ยวข้องกับเป้าหมายการประชุม
- อย่าสร้าง business rule ที่ไม่มีข้อมูลรองรับ
- แบ่งงานให้ Agent หลายคนเมื่อเหมาะสม

ตอบ JSON เท่านั้น:

{{
  "objective": "วัตถุประสงค์ของรอบ",
  "assignments": [
    {{
      "agent": "AI-2",
      "task": "งานที่ต้องทำ"
    }}
  ]
}}
"""

        response = chat(
            prompt,
            response_format="json",
        )

        return RoundPlan.model_validate_json(response)

    def execute_assignment(
        self,
        session: MeetingSession,
        assignment: Assignment,
    ) -> AgentResult:

        hat = session.current_hat

        prompt = f"""
/no_think

คุณเป็น Agent ใน AI Office

เป้าหมายการประชุม:
{session.goal}

Thinking Hat:
{hat}

กติกาของ Hat:
{HAT_GUIDANCE[hat]}

บทบาทของคุณ:
{self.role.value}

งานที่ได้รับ:
{assignment.task}

ทำเฉพาะงานที่ได้รับ

กฎ:
- อย่าออกนอกประเด็น
- อย่าสร้างข้อมูลที่ไม่มีหลักฐาน
- ถ้าไม่มีข้อมูลเพียงพอ ให้ระบุว่า "ยังไม่มีข้อมูลเพียงพอ"
- แยกข้อเท็จจริงออกจากข้อสันนิษฐาน
"""

        response = chat(prompt)

        return AgentResult(
            agent=self.name,
            response=response,
        )

    def execute_assignment(
        self,
        session: MeetingSession,
        assignment: Assignment,
        context: str | None = None,
    ) -> AgentResult:

        hat = session.current_hat

        context_text = ""

        if context:
            context_text = f"""
ข้อมูลจาก Agent ก่อนหน้า:

{context}

ให้นำข้อมูลนี้มาใช้ในการวิเคราะห์
แต่ต้องตรวจสอบเหตุผลด้วยตนเอง
"""

        prompt = f"""
/no_think

คุณเป็น Agent ใน AI Office

เป้าหมายการประชุม:
{session.goal}

Thinking Hat:
{hat}

กติกาของ Hat:
{HAT_GUIDANCE[hat]}

บทบาทของคุณ:
{self.role.value}

งานที่ได้รับ:
{assignment.task}

{context_text}

กฎ:
- ทำเฉพาะงานที่ได้รับ
- อย่าออกนอกประเด็น
- อย่าสร้างข้อมูลที่ไม่มีข้อมูลรองรับ
- ถ้าไม่มีข้อมูลเพียงพอ ให้ระบุว่า "ยังไม่มีข้อมูลเพียงพอ"
- แยกข้อเท็จจริงออกจากข้อสันนิษฐาน
"""

        response = chat(prompt)

        return AgentResult(
            agent=self.name,
            response=response,
        )

    def create_final_proposal(
        self,
        session: MeetingSession,
    ) -> FinalProposal:

        rounds_text = ""

        for index, meeting_round in enumerate(
            session.rounds,
            start=1,
        ):
            rounds_text += f"\n\n=== ROUND {index} : {meeting_round.hat} ===\n"
            rounds_text += f"Objective: {meeting_round.objective}\n"

            for result in meeting_round.results:
                rounds_text += (
                    f"\n[{result.agent}]\n"
                    f"{result.response}\n"
                )

        prompt = f"""
/no_think

คุณเป็น TEAM LEAD ของ AI Office

เป้าหมาย:
{session.goal}

ทีมได้ประชุมผ่าน Thinking Hats แล้ว

ข้อมูลทั้งหมดจากการประชุม:
{rounds_text}

หน้าที่:
สรุปผลการประชุมเป็น Final Proposal

ต้องมี:
1. summary
2. proposal

กฎ:
- แยกสิ่งที่ทีมรู้จริงออกจากข้อเสนอ
- ถ้ายังมีข้อมูลไม่เพียงพอ ให้ระบุอย่างชัดเจน
- อย่าสร้างข้อมูลใหม่
- ข้อเสนอควรสอดคล้องกับสิ่งที่ทีมค้นพบ

ตอบ JSON เท่านั้น:

{{
  "summary": "สรุปผลการประชุม",
  "proposal": "ข้อเสนอสุดท้าย"
}}
"""

        response = chat(
            prompt,
            response_format="json",
        )

        return FinalProposal.model_validate_json(response)

    def move_forward(
        self,
        session: MeetingSession,
    ) -> None:

        hat = self.hat_controller.move_forward()

        session.current_hat = hat.value

    def move_backward(
        self,
        session: MeetingSession,
    ) -> None:

        hat = self.hat_controller.move_backward()

        session.current_hat = hat.value