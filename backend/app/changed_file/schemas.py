from pydantic import BaseModel


class ChangedFileImportSummary(BaseModel):
    commit_id: int
    imported: int
