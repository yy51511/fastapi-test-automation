import { expect, test } from "@playwright/test"

test("Create and delete item end-to-end", async ({ page }) => {
  const title = `E2E Item ${Date.now()}`
  const description = "Created by Playwright E2E test"

  // 1. 进入 Items 页面
  await page.goto("/items")

  // 2. 创建 Item
  await page.getByRole("button", { name: "Add Item" }).click()

  await page.getByLabel("Title").fill(title)
  await page.getByLabel("Description").fill(description)

  await page.getByRole("button", { name: "Save" }).click()

  // 3. 验证创建成功
  await expect(
    page.getByText("Item created successfully"),
  ).toBeVisible()

  const itemRow = page
    .getByRole("row")
    .filter({ hasText: title })

  await expect(itemRow).toBeVisible()
  await expect(itemRow).toContainText(description)

  // 4. 删除刚创建的 Item
  await itemRow.getByRole("button").last().click()

  await page
    .getByRole("menuitem", { name: "Delete Item" })
    .click()

  await page
    .getByRole("button", { name: "Delete" })
    .click()

  // 5. 验证删除成功
  await expect(
    page.getByText("The item was deleted successfully"),
  ).toBeVisible()

  await expect(
    page.getByRole("row").filter({ hasText: title }),
  ).not.toBeVisible()
})