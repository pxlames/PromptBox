from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .db import get_db
from . import schemas, crud


algo_router = APIRouter(prefix="/algo", tags=["algo"])


# AlgoCategory API
@algo_router.get("/categories/", response_model=List[schemas.AlgoCategoryOut])
def list_algo_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """列表算法分类"""
    return crud.list_algo_categories(db, skip=skip, limit=limit)


@algo_router.get("/categories/{category_id}", response_model=schemas.AlgoCategoryOut)
def get_algo_category(category_id: int, db: Session = Depends(get_db)):
    """获取算法分类"""
    category = crud.get_algo_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Algorithm category not found")
    return category


@algo_router.post("/categories/", response_model=schemas.AlgoCategoryOut, status_code=201)
def create_algo_category(data: schemas.AlgoCategoryCreate, db: Session = Depends(get_db)):
    """创建算法分类"""
    return crud.create_algo_category(db, data)


@algo_router.put("/categories/{category_id}", response_model=schemas.AlgoCategoryOut)
def update_algo_category(category_id: int, data: schemas.AlgoCategoryUpdate, db: Session = Depends(get_db)):
    """更新算法分类"""
    category = crud.update_algo_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Algorithm category not found")
    return category


@algo_router.delete("/categories/{category_id}", status_code=204)
def delete_algo_category(category_id: int, db: Session = Depends(get_db)):
    """删除算法分类"""
    ok = crud.delete_algo_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Algorithm category not found")
    return None


# AlgoProblem API
@algo_router.get("/problems/", response_model=List[schemas.AlgoProblemOut])
def list_algo_problems(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    category_id: Optional[int] = Query(None, description="按分类筛选"),
    difficulty: Optional[str] = Query(None, description="按难度筛选：简单/中等/困难"),
    status: Optional[str] = Query(None, description="按状态筛选：未开始/已掌握/再复习"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db)
):
    """列表算法题目"""
    return crud.list_algo_problems(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        difficulty=difficulty,
        status=status,
        keyword=keyword
    )


@algo_router.get("/problems/{problem_id}", response_model=schemas.AlgoProblemOut)
def get_algo_problem(problem_id: int, db: Session = Depends(get_db)):
    """获取算法题目"""
    problem = crud.get_algo_problem(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Algorithm problem not found")
    return problem


@algo_router.post("/problems/", response_model=schemas.AlgoProblemOut, status_code=201)
def create_algo_problem(data: schemas.AlgoProblemCreate, db: Session = Depends(get_db)):
    """创建算法题目"""
    return crud.create_algo_problem(db, data)


@algo_router.put("/problems/{problem_id}", response_model=schemas.AlgoProblemOut)
def update_algo_problem(problem_id: int, data: schemas.AlgoProblemUpdate, db: Session = Depends(get_db)):
    """更新算法题目"""
    problem = crud.update_algo_problem(db, problem_id, data)
    if not problem:
        raise HTTPException(status_code=404, detail="Algorithm problem not found")
    return problem


@algo_router.delete("/problems/{problem_id}", status_code=204)
def delete_algo_problem(problem_id: int, db: Session = Depends(get_db)):
    """删除算法题目"""
    ok = crud.delete_algo_problem(db, problem_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Algorithm problem not found")
    return None


# AlgoSolution API
@algo_router.get("/problems/{problem_id}/solutions/", response_model=List[schemas.AlgoSolutionOut])
def list_algo_solutions(
    problem_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """列表算法题解（按题目ID）"""
    # 验证题目是否存在
    problem = crud.get_algo_problem(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Algorithm problem not found")
    return crud.list_algo_solutions(db, problem_id=problem_id, skip=skip, limit=limit)


@algo_router.get("/solutions/{solution_id}", response_model=schemas.AlgoSolutionOut)
def get_algo_solution(solution_id: int, db: Session = Depends(get_db)):
    """获取算法题解"""
    solution = crud.get_algo_solution(db, solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Algorithm solution not found")
    return solution


@algo_router.post("/solutions/", response_model=schemas.AlgoSolutionOut, status_code=201)
def create_algo_solution(data: schemas.AlgoSolutionCreate, db: Session = Depends(get_db)):
    """创建算法题解"""
    try:
        return crud.create_algo_solution(db, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建题解失败: {str(e)}")


@algo_router.put("/solutions/{solution_id}", response_model=schemas.AlgoSolutionOut)
def update_algo_solution(solution_id: int, data: schemas.AlgoSolutionUpdate, db: Session = Depends(get_db)):
    """更新算法题解"""
    solution = crud.update_algo_solution(db, solution_id, data)
    if not solution:
        raise HTTPException(status_code=404, detail="Algorithm solution not found")
    return solution


@algo_router.delete("/solutions/{solution_id}", status_code=204)
def delete_algo_solution(solution_id: int, db: Session = Depends(get_db)):
    """删除算法题解"""
    ok = crud.delete_algo_solution(db, solution_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Algorithm solution not found")
    return None

