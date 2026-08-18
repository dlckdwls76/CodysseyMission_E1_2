# Git 명령어 및 clone/pull 실습

이 문서는 과제에서 요구하는 Git 명령어 실행 실습

## 기본 명령어 7종

| 명령어         | 역할                                 | 실습 확인 |
| -------------- | ------------------------------------ | --------- |
| `git init`     | 현재 폴더를 Git 저장소로 초기화      | [ ]       |
| `git add`      | 변경 파일을 커밋할 준비 영역에 추가  | [ ]       |
| `git commit`   | 준비한 변경사항을 버전으로 기록      | [ ]       |
| `git push`     | 로컬 커밋을 GitHub에 업로드          | [ ]       |
| `git pull`     | GitHub의 최신 변경사항을 가져와 병합 | [ ]       |
| `git checkout` | 브랜치를 생성하거나 이동             | [ ]       |
| `git clone`    | 원격 저장소를 새 로컬 폴더로 복제    | [ ]       |

> 이미 GitHub 저장소를 `clone`한 폴더에서는 다시 `git init`할 필요가 없습니다. `git init` 실습은 별도의 연습 폴더에서 수행

## 브랜치 생성과 병합 확인

```bash
git checkout -b feature/practice
# 파일을 수정한 뒤
git add README.md
git commit -m "Docs: 브랜치 실습 내용 추가"
git checkout main
git merge feature/practice
git push origin main
```

![Git 브랜치 병합 기록](docs/screenshots/merge.png)

## clone과 pull 실습

기존 프로젝트 폴더와 같은 상위 폴더에서 실행합니다.

```bash
git clone https://github.com/dlckdwls76/CodysseyMission_E1_2.git CodysseyMission_E1_2_clone
cd CodysseyMission_E1_2_clone
```

복제된 폴더에서 README에 간단한 한 줄을 추가한 다음 실행합니다.

```bash
git add README.md
git commit -m "Docs: clone 실습 확인 문구 추가"
git push origin main
```

기존 작업 폴더로 이동하여 변경사항을 가져옵니다.

```bash
cd ../CodysseyMission_E1_2
git pull origin main
```

## 결과 확인과 캡처

```bash
git status
git log --oneline --graph --all --decorate
```

명령어와 출력 결과가 함께 보이도록 캡처하여 `docs/screenshots/git-log.png`로 저장
