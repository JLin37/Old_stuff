/* eslint-disable */
<template>
  <div id="contact" class="container">
    <br>
    <img id="img" src="./../assets/votewithvoice_transp bg_black logo_with name.png">
    <br>
    <h1><b>Get Your Statement Heard</b></h1>
    <br>
    <br>
    <div class="row vdivide">
      <div id="googleMap" class="col-md-6">
        <google-map></google-map>
      </div>
      <div id="contactInfo" class="col-md-6">
        <address>
          111 John Street | Suite 420<br>
          New York, NY 10038<br>
        </address>
        <br>
        <a href="tel: +1-877-977-7786"><b> +1 (877)977-7786</b></a>
        <br/>
        <b>info@votewithvoice.com</b>
        <br/>
      </div>
    </div>
  </div>
</template>

<script>
import GoogleMap from './GoogleMap';

export default {
  name: 'ContactPage',
  data() {
    return {
      data: {
      },
    };
  },
  components: {
    GoogleMap,
  },
};

</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  
#googleMap {
  width: 100%;
}

.row.vdivide [class*='col-']:not(:last-child):after {
  background: black;
  width: 2px;
  content: "";
  display: block;
  position: absolute;
  top:0;
  bottom: 0;
  right: 0;
  min-height: 70px;
}

h1 {
  font-weight: bold;
  font-size: 48px;
}

#contactInfo {
  text-align: center;
  padding: 30px 30px 30px 30px;
  font-size: 24px;
}
#contactInfo > a{
  color: black;
}

#img {
  margin-top: 80px;
  padding: 80px;
  position: center;
  max-height: 300px;
  max-width: 100%;
}

.extra_padding{
  padding-bottom: 50px;
}

</style>
