# HumHub User Bulk Upload Script

This Python script allows you to automatically create users in **HumHub** via its API using data from an Excel file.

---

## 📂 Excel File Format (`users.xlsx`)

The Excel file must be in `.xlsx` format and contain the following **required columns** (column headers must match exactly):

| First Name [Required] | Last Name [Required] | Email Address [Required] | Recovery Phone [MUST BE IN THE E.164 FORMAT] |
| --------------------- | -------------------- | ------------------------ | -------------------------------------------- |
| Test1                 | User1                | testuser1@gmail.com      | +88005553535                                 |
| Test2                 | User2                | testuser2@gmail.com      | +88005553535                                 |

- Only the columns above are required. Other columns will be ignored.
- The **Recovery Phone** column is optional.
- Passwords will be **auto-generated**, so no password column is needed.

---

## ⚙️ Prerequisites

Install the required Python packages:

```bash
pip install pandas requests tqdm openpyxl
```
