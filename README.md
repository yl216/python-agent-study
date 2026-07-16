# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 13，计划管理增强。

## 安装依赖

```powershell
pip install -r requirements.txt
```

## 配置 DeepSeek

复制 `.env.example` 为 `.env`，然后把 `DEEPSEEK_API_KEY` 改成你的真实 DeepSeek API Key。

```powershell
Copy-Item .env.example .env
```

## 运行方式

```powershell
python src/main.py
```

## 当前命令

```text
/help                    查看帮助
/modes                   查看可用模式
/mode <name>             切换模式，并加载当前计划下该模式的对话历史
/clear                   清空当前计划 + 当前模式的对话记忆
/tools                   查看可用本地工具
/tool <命令>             手动调用本地工具
/intent <请求>           让模型输出 JSON 意图并自动调用工具
/plan <目标>             新建学习计划
/plans                   查看所有保存的计划
/plan-use <id>           切换当前计划
/plan-show               查看当前计划
/plan-next               标记当前步骤完成
/plan-rename <id> <名称> 重命名计划，计划 ID 也会改为新名称的 slug
/plan-done <id>          标记计划完成
/plan-archive <id>       归档计划
/plan-export <id>        导出计划为 Markdown
/plan-reset              取消当前激活计划，不删除历史计划文件
/plan-delete <id>        预览删除计划
/plan-delete <id> --yes  确认删除计划和该计划下所有 mode 对话
/exit                    退出程序
```

## 计划管理

计划列表会显示：

```text
计划 ID | 状态 | 进度 | 目标
```

状态包括：

```text
active
done
archived
```

重命名计划会同时更新：

- 计划目标名称
- 计划 ID
- `data/plans/<id>.json` 文件名
- `data/conversations/<id>/` 对话目录
- 如果它是当前激活计划，也会同步 active 指针

例如：

```text
/plan-rename 20260716013923-learn-functions learn
```

会把计划 ID 改成：

```text
learn
```

删除计划需要确认。第一次输入：

```text
/plan-delete <id>
```

只会显示影响范围，包括计划文件和每个 mode 下的对话消息数量。确认删除必须输入：

```text
/plan-delete <id> --yes
```

## 导出

计划可以导出为 Markdown：

```text
/plan-export <id>
```

导出文件位于：

```text
data/plan_exports/<id>.md
```

导出文件属于本地运行产物，不提交到 GitHub。

## 当前文件

- `src/main.py`：命令行入口、命令处理、工具、意图、计划、模式和对话历史路由。
- `src/planner.py`：学习任务规划、状态管理、导出、多计划保存和恢复。
- `src/conversation_store.py`：按计划和 mode 保存、加载、清空对话历史。
- `src/intent_parser.py`：让模型输出 JSON，并解析为 `intent` 和 `argument`。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
