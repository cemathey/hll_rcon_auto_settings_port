import json

from flask import Flask, render_template, request
from loguru import logger
from wtforms import Form, SelectField, TextAreaField, validators

from hll_rcon_auto_settings_port.constants import Versions
from hll_rcon_auto_settings_port.utils import upgrade

logger.add("debug.log", mode="w")

app = Flask(__name__)


class ConvertForm(Form):
    from_version = SelectField(
        label="Select the version you are migrating from",
        choices=[v.value.strip() for v in Versions if v],
        validators=[validators.DataRequired()],
    )
    to_version = SelectField(
        label="Select the version you are migrating to",
        choices=[v.value.strip() for v in Versions if v],
        validators=[validators.DataRequired()],
    )
    settings = TextAreaField(
        label="Old Auto Settings", validators=[validators.DataRequired()]
    )

    def validate(self):
        print(f"Validating")
        if not Form.validate(self):
            return False
        print(f"Validating...")

        print(f"{self.from_version.data=} {self.to_version.data=}")
        if self.to_version.data == self.from_version.data:
            self.from_version.errors.append("To/From versions must be different")
            self.to_version.errors.append("To/From versions must be different")
            return False

        return True


@app.route("/", methods=["GET", "POST"])
def hello_world():
    form = ConvertForm(request.form)

    new_settings = None
    if request.method == "POST" and form.validate():
        from_version = form.from_version.data
        to_version = form.to_version.data
        old_settings = json.loads(form.settings.data)
        new_settings = upgrade(
            from_version=from_version, to_version=to_version, payload=old_settings
        )

    if new_settings:
        new_settings = json.dumps(new_settings, indent=2)
    else:
        new_settings = ""

    if app.debug:
        with open("dump.json", "w") as fp:
            fp.write(new_settings)

    return render_template("index.html", form=form, new_settings=new_settings)
