# Galmuri Bold Fix

Minecraft Java 26.3 + Fabric에서 갈무리 TTF의 볼드가 두 겹으로 보이는 현상을 줄이는 클라이언트 모드입니다. 리소스팩만 사용해도 폰트 교체는 동작하며, 이 모드는 선택 사항입니다.

## 동작

Minecraft 26.3은 일반 TTF 볼드를 오른쪽으로 1 GUI 픽셀 이동해 한 번 더 그립니다. 이 모드는 폰트 내부 family 이름이 `Galmuri`로 시작하는 경우에만 이동 간격과 볼드 추가 폭을 0.5 GUI 픽셀로 줄입니다. 원본 폰트 파일, 일반 글자 폭, 그림자 간격은 유지합니다. 비트맵 폰트와 다른 TTF에는 적용하지 않습니다.

0.25픽셀은 게임 내 비교에서 굵기 차이가 약했고, 최종값 0.5픽셀로 확인했습니다. Mixin 클래스는 `local.galmuri.mixin`, 일반 런타임 클래스는 `local.galmuri.font`에 분리합니다.

## 지원 환경

- Minecraft Java **26.3**
- Fabric Loader **0.20.1 이상**
- Java **25 이상** (빌드는 JDK 필요)
- Fabric API는 필요하지 않습니다.

리소스팩의 지원 범위와 모드의 지원 범위는 다릅니다. 모드는 26.4 스냅샷에서 검증하지 않았고, 게임 내부 코드를 수정하므로 26.3에만 로딩되도록 제한했습니다.

## 빌드

Python 3와 JDK 25 이상이 필요합니다. Minecraft 26.3 Fabric 프로필을 먼저 실행해 클라이언트와 라이브러리를 준비합니다.

저장소 루트에서 실행합니다. `--minecraft-dir`에는 `versions`와 `libraries` 폴더가 있는 Minecraft 디렉토리를 전달합니다.

```sh
python3 mods/galmuri-bold-fix/build.py --minecraft-dir "/path/to/minecraft"
```

스크립트는 설치된 클라이언트와 라이브러리로 컴파일하고, 일반 글자 폭·그림자 유지, 볼드 0.5픽셀, Mixin 패키지 분리를 검사합니다. 게임 내 로딩 검사를 대신하지는 않습니다. Minecraft 파일은 결과물에 포함하지 않습니다.

JDK가 여러 개라면 `--java-home "/path/to/jdk-25"`를 추가하거나 `JAVA_HOME`으로 JDK 25 이상을 선택합니다.

결과물: `mods/galmuri-bold-fix/dist/galmuri-bold-fix-1.0.2.jar`

## 설치 및 비교

1. 게임을 완전히 종료합니다.
2. 빌드된 JAR을 Minecraft 디렉토리의 `mods`에 넣습니다. 이전 `galmuri-bold-fix` JAR이 있다면 폴더 밖으로 옮겨 한 버전만 남깁니다.
3. Fabric 26.3으로 실행하고 이 저장소의 갈무리 리소스팩을 활성화합니다.
4. OP 권한이 있는 채팅에서 아래 명령어로 비교합니다. 위가 일반, 아래가 볼드입니다.

```mcfunction
/tellraw @s [{"text":"가나다라 한글 테스트\n","bold":false},{"text":"가나다라 한글 테스트","bold":true}]
```

모드 변경은 F3+T로 적용되지 않으며 게임을 재시작해야 합니다. 되돌리려면 게임을 종료하고 이 모드 JAR을 `mods` 폴더 밖으로 옮깁니다.
