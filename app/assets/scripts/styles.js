import Style from 'ol/style/style';
import Fill from 'ol/style/fill';
import Text from 'ol/style/text';
import Stroke from 'ol/style/stroke';
import Circle from 'ol/style/circle';

const stopStyle = new Style({
  image: new Circle({
    fill: new Fill({
      color: '#FFF'
    }),
    stroke: new Stroke({
      color: '#000',
      width: 2
    }),
    radius: 5
  }),
});

const selectedStopStyle = new Style({
  image: new Circle({
    fill: new Fill({
      color: '#F00'
    }),
    stroke: new Stroke({
      color: '#000',
      width: 2
    }),
    radius: 6
  })
});

const labelStyle = new Style({
  text: new Text({
    font: '14px Calibri,sans-serif',
    fill: new Fill({
      color: '#000'
    }),
    stroke: new Stroke({
      color: '#fff',
      width: 2
    }),
    offsetX: 15,
    offsetY: 15
  })
});

export {
  stopStyle,
  selectedStopStyle,
  labelStyle
};
