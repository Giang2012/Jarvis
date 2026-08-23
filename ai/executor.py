class Executor:

    def __init__(self, planner):

        self.planner = planner

    def execute(self, plan):

        results = []

        for task in plan:

            try:

                result = self.planner.execute(
                    task.action,
                    task.target
                )

                results.append(result)

            except Exception as e:

                results.append(
                    f"Task {task.action} failed: {e}"
                )

        return results