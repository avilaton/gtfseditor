import json
from flask_script import Command

from app import db
from app.models import Shape
from app.models import ShapePath

class MigrateShapes(Command):
    """Migrates shapes to shape_paths"""

    def run(self):
        ShapePath.query.delete()
        db.session.commit()

        for row in db.session.query(Shape.shape_id).distinct().all():
            path = Shape.get_vertices_array(row.shape_id)
            shape_path = ShapePath(shape_id=row.shape_id, shape_path=json.dumps(path))
            db.session.add(shape_path)
            db.session.commit()

        db.session.execute("""SELECT setval('shape_paths_shape_id_seq', (
            SELECT MAX(shape_id) FROM shape_paths
            ));""")
