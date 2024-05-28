from backend.extensions import db
import sqlalchemy.orm as so
import sqlalchemy as sa


class File(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    path: so.Mapped[str] = so.mapped_column(sa.String(150))
    filename: so.Mapped[str] = so.mapped_column(sa.Text)
    filesize: so.Mapped[int] = so.mapped_column(sa.Integer)
    filetype: so.Mapped[str] = so.mapped_column(sa.Text)

    def __repr__(self):
        return f'<File "{self.filename}">'

    def to_dict(self):
        return {
            "path": self.path,
            "filename": self.filename,
            "filesize": self.filesize,
            "filetype": self.filetype,
        }
