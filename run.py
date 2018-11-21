from laptop import app,db
from laptop.models import User, Applications, LapMod , Graphics, Processor, Memory, Battery, application

if __name__ == '__main__':
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Applications': Applications,"LapMod":LapMod,  "Graphics":Graphics,
            "Processor":Processor,"Memory":Memory,"Battery":Battery, "application":application}
