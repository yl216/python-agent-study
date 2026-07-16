# 第 18 次学习：测试边界情况

这一阶段学习的是：不要只测试顺利的情况，还要测试容易出错的边界。

正常流程测试能告诉我们“功能可以工作”。边界测试能告诉我们“用户乱输、重复操作、数据不存在时，程序不会悄悄坏掉”。

## 新增测试

测试文件仍然是：

```text
tests/test_plan_management.py
```

本次新增 4 个测试：

- 重命名为空名称应该抛出 `ValueError`
- 重命名成已经存在的名称时，新 ID 应该自动变成 `learn-functions-2`
- 删除不存在的计划应该返回 `False`
- 清空一个 mode 的对话时，不应该影响同计划下其他 mode 的对话

## 为什么这些重要

计划系统里有三类状态：

- 计划文件：`data/plans/<id>.json`
- 当前计划指针：`data/active_plan.json`
- 对话历史：`data/conversations/<plan_id>/<mode>.json`

越是有多份状态，越需要边界测试。因为最常见的 bug 不是“完全不能用”，而是“某一份状态忘了同步”。

## 运行方式

```powershell
python -m unittest discover -s tests
```

如果看到类似：

```text
Ran 6 tests
OK
```

说明目前计划管理的核心流程和边界情况都被测试保护住了。
