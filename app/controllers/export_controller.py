import openpyxl
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.valoracion import Valoracion


async def exportar_excel(bono_id: int, db: AsyncSession):
    stmt = select(Valoracion).where(Valoracion.bono_id == bono_id)
    result = await db.execute(stmt)
    valoraciones = result.scalars().all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Valoraciones"

    headers = [
        "Fecha",
        "TCEA",
        "TREA",
        "Duración",
        "Dur. Modificada",
        "Convexidad",
        "Precio Máximo",
        "Origen",
        "Valor Base",
        "Precio Calculado",
        "TIR",
    ]
    ws.append(headers)

    for v in valoraciones:
        ws.append(
            [
                v.fecha_valoracion,
                v.tcea,
                v.trea,
                v.duracion,
                v.duracion_modificada,
                v.convexidad,
                v.precio_maximo,
                v.origen_valoracion,
                v.valor_base,
                v.precio_calculado,
                v.tir_calculada,
            ]
        )

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=valoraciones_bono_{bono_id}.xlsx"
        },
    )
