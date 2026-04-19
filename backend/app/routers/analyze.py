from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.analysis import Analysis
from app.services.file_parser import extract_text
from app.services.ai_service import generate_academic_outputs

router = APIRouter(prefix='/api', tags=['analysis'])


@router.get('/health')
def health_check():
    return {'status': 'ok'}


@router.get('/history')
def get_history(db: Session = Depends(get_db)):
    rows = db.query(Analysis).order_by(Analysis.id.desc()).all()
    return rows


@router.post('/analyze')
async def analyze_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        text = extract_text(file.filename, content)
        if not text.strip():
            raise HTTPException(status_code=400, detail='No extractable text found in the file.')

        outputs = generate_academic_outputs(text)
        row = Analysis(
            filename=file.filename,
            summary=outputs['summary'],
            questions=outputs['questions'],
            rubric=outputs['rubric'],
            study_plan=outputs['study_plan'],
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
