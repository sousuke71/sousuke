# demo.py
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

from hcaptcha_challenger import AgentV, AgentConfig

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="tmp_user_data",
            headless=False,
            record_video_dir=Path("recordings"),
            record_video_size={"width": 1920, "height": 1080},
        )

        page = await context.new_page()
        await page.goto("https://accounts.hcaptcha.com/demo")

        # Agent初期化
        agent = AgentV(page=page, agent_config=AgentConfig())

        # チェックボックスクリックでチャレンジ開始
        await agent.robotic_arm.click_checkbox()
        await agent.wait_for_challenge()

        # 結果表示（成功したらトークンが出る）
        if agent.cr_list:
            print(json.dumps(agent.cr_list[-1].model_dump(by_alias=True), indent=2))

        await asyncio.sleep(15)  # 録画をしっかり残す
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
