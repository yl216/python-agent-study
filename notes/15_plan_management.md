# 第 15 次学习：计划管理增强

今天的目标是让计划不只是能保存，还能更好地管理。

## 新增能力

- 重命名计划。
- 标记计划完成。
- 归档计划。
- 导出计划为 Markdown。
- 删除计划前显示更详细的影响范围。

## 新增命令

```text
/plan-rename <id> <名称>
/plan-done <id>
/plan-archive <id>
/plan-export <id>
/plan-delete <id>
/plan-delete <id> --yes
```

## 删除影响预览

删除计划前，程序会显示：

- 将删除哪个计划文件。
- 该计划下有哪些 mode 对话。
- 每个 mode 有多少条消息。

只有带 `--yes` 才会真正删除。

## 状态管理

计划现在有状态：

```text
active
done
archived
```

这让计划列表更容易扫描。

## 导出 Markdown

`/plan-export <id>` 会把计划导出到：

```text
data/plan_exports/<id>.md
```

导出文件是本地运行产物，不提交到 GitHub。

## 本阶段验收

1. 能创建计划。
2. 能重命名计划。
3. 能标记完成。
4. 能归档。
5. 能导出 Markdown。
6. 删除前能看到影响范围。
7. 删除必须使用 `--yes` 才会执行。
