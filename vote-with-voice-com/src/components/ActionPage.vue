/* eslint-disable */
<template>
  <div id="actionPage">
    <br>
    <img id="img" src="./../assets/votewithvoice_transp bg_black logo_with name.png">
    <br>
    <div class="extra_padding"></div>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
      <input type="hidden" name="cmd" value="_s-xclick">
      <input type="hidden" name="hosted_button_id" value="WT7436WYU9VES">
      <table class="center">
        <tr><td><input type="hidden" name="on0" value="Candidate Name">Candidate Name</td></tr>
        <tr><td><input class="color" type="text" name="os0" maxlength="200"></td></tr>
        <tr><td><input type="hidden" name="on1" value="Candidate State">Candidate State</td></tr>
        <tr><td><input class="color" type="text" name="os1" maxlength="200"></td></tr>
      </table>
      <br>
      <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_paynowCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
      <img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
    </form>
    <br />
  </div>
</template>

<script>
export default {
  name: 'ActionPage',
  data() {
    return {
      el: 'body',
      data: {
      },
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#img {
  margin-top: 80px;
  padding: 80px;
  position: center;
  max-height: 300px;
  max-width: 100%;
}

table.center {
    margin-left: auto;
    margin-right: auto;
}
input.color {
    background-color: white;
}
.fab {
    font-size: 80px;
    color: white;
}
h1, h2 {
    color: white;
    position: center;
}
ul {
    position: center;
}
li {
    display: inline-block;
    margin: 50px 50px 0 0;
}

.extra_padding{
  padding-bottom: 50px;
}

#vote_logo{
  padding-bottom: 100px;
}

</style>