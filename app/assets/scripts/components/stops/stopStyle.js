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

export {stopStyle};
