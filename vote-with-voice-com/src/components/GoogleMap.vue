<template>
  <div>
    <gmap-map
      :center='center'
      :zoom='12'
      style='width:80%;  height: 350px;'
    >
      <gmap-marker :position='marker'>
      </gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
export default {
  name: 'GoogleMap',
  data() {
    return {
      center: { lat: 40.730824, lng: -73.997330 },
      marker: { lat: 40.7076789, lng: -74.0057 }
    };
  },

  mounted() {
    this.geolocate(this.center);
  },

  methods: {
    geolocate() {
      navigator.geolocation.getCurrentPosition((position) => {
        this.center = {
          lat: this.center.lat,
          lng: this.center.lng,
        };
      });
    },
  },
};
</script>
