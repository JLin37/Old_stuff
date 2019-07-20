<template>
  <div id="app" class="container-fluid">
    <Slide right noOverlay id="menu">
      <router-link tag="a" to="/">
        <span>Home</span>
      </router-link>
      <router-link tag="a" to="/info">
        <span>What We Do?</span>
      </router-link>
      <!-- <router-link tag="a" to="/action">
        <span>Get involved</span> -->
      </router-link>
      <router-link tag="a" to="/contact">
        <span>Contact</span>
      </router-link>

      <footer id="footer">
        <div class = "container footer">
          <div class="row">
            <div class="col-md-3 text-center">
                <a href="https://twitter.com/votewithvoice" target="_blank"> <i class="fab fa-twitter fa-2x"></i></a>
            </div>
            <div class="col-md-3 text-center">
                <a href="https://www.facebook.com/Vote-with-Voice-438189039920417" target="_blank"><i class="fab fa-facebook-f fa-2x"></i></a>
            </div>
            <div class="col-md-3 text-center">
                <a href="https://www.instagram.com/votewithvoice" target="_blank"><i class="fab fa-instagram fa-2x"></i></a>
            </div>
            <div class="col-md-3 text-center">
                <a href="https://www.linkedin.com/company/vote-with-voice" target="_blank"><i class="fab fa-linkedin fa-2x"></i></a>
            </div>
          </div>
          <br>
          <div>
              <a href="/privacy">
                Privacy Policy
              </a>
              <br>
              <a href="/politicalad">
                Political Advertising Guidelines
              </a>
              </span></span>
          </div>
          <br>
        </div>
      </footer>
    </Slide>
    <router-view></router-view>
  </div>
</template>

<script>
import { Slide } from 'vue-burger-menu'  // import the CSS transitions you wish to use, in this case we are using `Slide`

export default {
  name: 'App',

  components: {
          Slide // Register your component
      },
};
</script>

<style>
#app {
  font-family: 'Montserrat', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
}

.text-center {
  text-align: center;
}

.bm-cross-button {
  height: 30px;
  width: 30px;
}

.footer {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 1rem;
  text-align: center;
}

.footer > * > a {
  color: white;
}

.footer > * > a {
  color: white;
  font-weight: 500;
}

.fab {
  color: white;
}

</style>
