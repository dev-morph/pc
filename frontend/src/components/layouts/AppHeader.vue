<template>
    <header>
        <nav class="wrapper">
            <RouterLink to="/"><span class="link">Home</span></RouterLink>
            <RouterLink to="/about"><span class="link">About</span></RouterLink>
        </nav>
    </header>
</template>

<style scoped lang="scss">
.wrapper {
    background: #1c1c1e;
    display: flex;
    justify-content: center;
    gap: 1rem;
    align-items: center;
    padding: 1rem 0;

    a {
        &.router-link-exact-active {
            span {
                color: white; // 활성 상태일 때 span 색상 변경
            }
        }
        .link {
            display: inline-block;
            width: 100%;
            position: relative;
            color: gray;
            &:after {
                content: "";
                position: absolute;
                bottom: -1rem;
                left: 0;
                width: 100%;
                height: 2px;
                background: white;
                transform: scaleX(0);
                transform-origin: center;
                transition: transform 0.2s ease;
            }
            &:hover {
                &:after {
                    transform: scaleX(1);
                    transform-origin: center;
                }
            }
        }
    }
}
</style>
