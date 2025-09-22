<template>
    <!-- <div v-cloak class="f6inject"> -->
    <div v-cloak>
        <div class="container-fluid">
            <!-- First Row: Search Panel and Map -->
            <div class="row">
                <!-- Left Column (Search Panel) -->
                <div class="col-lg-3">
                    <!-- The content of the original left column will go here -->
                    <div class="columns small-12 medium-12 large-12" v-show="current_booking.length > 0">
                        <div class="row">
                            <div class="columns small-12 medium-12 large-12" >
                                <button  title="Please add items into your trolley." v-show="ongoing_booking" style="color: #FFFFFF; background-color: rgb(255, 0, 0); margin-right:10px;" class="button small-12 medium-12 large-12" >Time Left {{ timeleft }}</button>
                                <a v-show="current_booking.length > 0" class="button small-12 medium-12 large-12" :href="parkstayUrl+'/booking'" style="border-radius: 4px; border: 1px solid #2e6da4">Proceed to Check Out</a> <a type="button" :href="parkstayUrl+'/booking/abort'" class="button float-right warning continueBooking" style="color: #fff; background-color: #f0ad4e;  border-color: #eea236; border-radius: 4px;">
                                    Cancel in-progress booking
                                </a>
                            </div>
                            <div class="small-12 medium-12 large-12">
                                <div class="card">
                                    <div class="card-body"><h3 class="card-title">Trolley: <span id='total_trolley'>${{ total_booking }}</span></h3></div>
                                </div>
                                <div class='columns small-12 medium-12 large-12' style="margin-top:10px; margin-bottom:10px;">
                                        <div v-for="item in current_booking" class="row small-12 medium-12 large-12">
                                                <div class="columns small-12 medium-9 large-9">{{ item.item }}</div>
                                                <div class="columns small-12 medium-2 large-2">${{ item.amount }}</div>
                                                <div class="columns small-12 medium-1 large-1"><a v-show="item.past_booking == false" style='color: red; opacity: 1;' type="button" class="close" @click="deleteBooking(item.id)">x</a></div>
                                        </div>
                                </div>
                            </div>
                        </div>
                    </div>

                        <div class="row">
                            <div class="small-12 columns">
                                <label>Search <input class="input-group-field" id="searchInput" type="text" placeholder="Search for a mooring..."/></label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="small-12 medium-12 large-6 columns">
                                <label for="dateArrival">Arrival</label>
                                <input
                                    type="date"
                                    id="dateArrival"
                                    v-model="arrivalDateForInput"
                                    :min="minArrivalDateForInput"
                                    @change="handleArrivalDateChange"
                                >
                            </div>
                            <div class="small-12 medium-12 large-6 columns">
                                <label for="dateDeparture">Departure</label>
                                <input
                                    type="date"
                                    id="dateDeparture"
                                    v-model="departureDateForInput"
                                    :min="minDepartureDateForInput"
                                >
                            </div>
                            
                            <div class="small-12 medium-12 large-12 columns" style="display:none;">
                                <label><input type="checkbox" v-model="bookableOnly"/> Show bookable moorings only</label>
                            </div>
                        </div>
                        <div class="row"><div class="small-12 columns">
                            <hr/>
                        </div>
                        </div>
                        <div class="row">
                            <div class="small-12 medium-12 large-6 columns">
                            <label>Vessel Registration  <input v-model="vesselRego" id="vesselRego" name="vessel_rego" type="text" placeholder="REGO134" :disabled="current_booking.length > 0" step='0.01' /></label>
                            </div>
                            <div class="small-12 medium-12 large-6 columns">
                            <label>Vessel Size (Meters) <input v-model="vesselSize" id="vesselSize" name="vessel_size" type="number" placeholder="35" :disabled="current_booking.length > 0" step='0.01' /></label>
                            </div>
                            <div class="small-12 medium-12 large-6 columns">
                            <label>Vessel Draft (Meters) <input v-model="vesselDraft" id="vesselDraft" name="vessel_draft" type="number" placeholder="10" :disabled="current_booking.length > 0" step='0.01' /></label>
                            </div>
                            <div class="small-12 medium-12 large-6 columns">
                            <label>Vessel Beams (Meters)  <input v-model="vesselBeam" id="vesselBeam" name="vessel_beams" type="number" placeholder="3" :disabled="current_booking.length > 0" step='0.01' /></label>
                            </div>
                            <div class="small-12 medium-12 large-6 columns">
                            <label>Vessel Weight (Tonnes)  <input v-model="vesselWeight" id="vesselWeight" name="vessel_weight" type="number" placeholder="2" :disabled="current_booking.length > 0" step='0.01' /></label>
                            </div>
                            <div class="small-12 medium-12 large-6 columns" >
                                <label>
                                    Guests <input type="button" class="button formButton" v-bind:value="numPeople" data-toggle="guests-dropdown"/>
                                </label>
                                <div class="dropdown-pane" id="guests-dropdown" data-dropdown data-auto-focus="true">
                                    <div class="row">
                                        <div class="small-6 columns">
                                            <label for="num_adults" class="text-right">Adults</label>
                                        </div>
                                        <div class="small-6 columns">
                                            <input type="number" id="numAdults" name="num_adults" v-model="numAdults" min="0" max="16"/>
                                        </div>
                                    </div>
                                    <div class="row" style="display:none;">
                                        <div class="small-6 columns">
                                            <label for="num_concessions" class="text-right"><span class="has-tip" title="Holders of one of the following Australian-issued cards:
                                                - Seniors Card
                                                - Age Pension
                                                - Disability Support
                                                - Carer Payment
                                                - Carer Allowance
                                                - Companion Card
                                                - Department of Veterans' Affairs">Concessions</span>
                                            </label>
                                        </div><div class="small-6 columns">
                                            <input type="number" id="numConcessions" name="num_concessions" v-model="numConcessions" min="0" max="16"/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="small-6 columns">
                                            <label for="num_children" class="text-right">Children (4-16)</label>
                                        </div>
                                        <div class="small-6 columns">
                                            <input type="number" id="numChildren" name="num_children" v-model="numChildren" min="0" max="16"/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="small-6 columns">
                                            <label for="num_children" class="text-right">Infants (under 4)</label>
                                        </div>
                                        <div class="small-6 columns">
                                            <input type="number" id="numInfants" name="num_infants" v-model="numInfants" min="0" max="16"/>
                                        </div>
                                    </div>
                                    <div class="row" style="display:none;">
                                        <div class="small-6 columns">
                                            <label for="num_children" class="text-right">Moorings</label>
                                        </div>
                                        <div class="small-6 columns">
                                            <input type="number" id="numMooring" name="num_mooring" v-model="numMooring" min="0" max="16"/>
                                        </div>
                                    </div>
                            </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="small-12 columns">
                            <hr/>
                            </div>
                        </div>
                        <div class="row">
                            <div class="small-12 medium-12 large-12 columns">
                                <label>Mooring</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="gear_type" value="all" v-model="gearType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC3"></i> All types</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="gear_type" value="rental-available" v-model="gearType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Rental (available)</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="gear_type" value="rental-notavailable" v-model="gearType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Rental (not available)</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="gear_type" value="public-notbookable" v-model="gearType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Public (not bookable)</label>
                            </div>
                        </div>

                        <div class="row">
                            <div class="small-12 columns">
                                <hr/>
                            </div>
                        </div>
                        <div class="row">
                            <div class="small-12 medium-12 large-12 columns">
                                <label>Types</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="pen_type" value="all" v-model="penType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC3"></i> All types</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="pen_type" value="0" v-model="penType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Moorings</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="pen_type" value="1" v-model="penType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Jetty Pens</label>
                            </div>
                            <div class="small-12 medium-12 large-4 columns">
                                <label><input type="radio" name="pen_type" value="2" v-model="penType" class="show-for-sr" v-on:change="reload()"/><i class="symb RC20"></i> Beach Pens</label>
                            </div>
                        </div>

                        <hr class="search"/>

                        <div class="row" id="legend" style="margin-bottom:10px;">
                            <div class="small-12 medium-12 large-12 columns">
                                <label>Availability</label>
                            </div>
                            <div class="small-12 medium-12 large-3 columns">
                                <label>Public:
                                    <img class="publicPin" :src="pin_gray" />
                                </label>
                            </div>
                            <div class="small-12 medium-12 large-3 columns">
                                <label>Available:
                                    <img class="availablePin" :src="pin_orange" />
                                </label>
                            </div>
                            <div class="small-12 medium-12 large-3 columns">
                                <label>Partial Dates:
                                    <img class="partialPin" :src="pin_orange_red" />
                                </label>
                            </div>
                            <div class="small-12 medium-12 large-3 columns">
                                <label>Unavailable:
                                    <img class="unavailablePin" :src="pin_red" />
                                </label>
                            </div>
                        </div>

                        <div class="row"><div class="small-12 columns">
                            <hr class="search"/>
                        </div>
                        <div class="row" style='display:none'>
                            <div class="small-12 medium-12 large-12 columns">
                                <label>Select features</label>
                            </div>
                            <template v-for="filt in filterList">
                                <div class="small-12 medium-12 large-4 columns">
                                    <label><input type="checkbox" class="show-for-sr" :value="'filt_'+ filt.key" v-model="filterParams[filt.key]" v-on:change="updateFilter()"/> <i class="symb" :class="filt.symb"></i> {{ filt.name }}</label>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Right Column (Map) -->
                <div class="col-lg-9">
                    <!-- The content of the original right column will go here -->
                    <div class="alert alert-warning" style='text-align: center' role="alert" v-if="admissions_key" id="admissions_link">
                        <strong style='font-size: 16px;'>
                            <a :href='"/annual-admissions/" + admissions_key + "/"'>Click here for paying annual admission fees only</a>
                        </strong><br>
                    </div>   
                    <div class="alert alert-warning" style='text-align: center' role="alert" v-if="admissions_key" id="admissions_link">
                        <strong style='font-size: 16px;'>
                            <a :href='"/admissions/" + admissions_key + "/"'>Click here for paying individual admission fees for a single visit</a>
                        </strong><br>
                    </div>
                    <div class="alert alert-info" style='text-align: center' role="alert" v-if="admissions_key" id="admissions_link">
                        <strong style='font-size: 16px;'>
                            <a href='https://rottnestisland.com/boating/Fees'>Click here for more information on admission fees</a>
                        </strong><br>
                    </div>
                    <div style='width: 100%; height: 1px;' align='right'>
                        <div v-show='mapLoading == true' class='map-loading' style='border: 1px solid #00000'>
                            <img style='width:20px; height: 20px;' src='@/assets/ajax-loader-spinner.gif'>&nbsp;&nbsp;Please Wait
                        </div>
                    </div>
                    <div id="map"></div>
                    <div style='width: 100%' align='right'>
                        <img id='satellite-toggle' class='map-toggle-white'  type='button'  @click="toggleMap('satellite');" src='./assets/img/satellite_icon.png' />
                        <img id='map-toggle' class='map-toggle-black'  type='button'  @click="toggleMap('map');" src='./assets/img/map_icon.png' />
                    </div>
                    <div id="mapPopup" class="mapPopup" v-cloak>
                        <a href="#" id="mapPopupClose" class="mapPopupClose"></a>
                        <div id="mapPopupContent">
                            <h4 style="margin: 0"><b id="mapPopupName"></b></h4>
                            <p><i id="mapPopupPrice"></i></p>
                            <img class="thumbnail" id="mapPopupImage" style='width: 230px; height: 230px;' />
                            <div id="mapPopupDescription" style="font-size: 0.75rem;"/>
                            <p>Mooring Limits</p>
                            <div class="row">
                                <div class="col-md-7"  style='display:none'>
                                    <small>Max Stay: <span id='max_stay_period'></span> day/s</small>
                                </div>
                                <div class="col-md-5">
                                    <small>Max Size: <span id='vessel_size_popup'></span></small>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-7">
                                    <small>Max Draft: <span id='vessel_draft_popup'></span></small>
                                </div>
                                <div class="col-md-5">
                                    <small><span id='vessel_beam_weight_popup'></span></small>
                                </div>
                            </div>
                            <input id='mapPopupMooringType' type='hidden' >
                            <a id="mapPopupInfo" class="button formButton" style="margin-bottom: 0; margin-top: 1em;" target="_blank">More info</a>
                            <a id="mapPopupBook" class="button formButton" style="margin-bottom: 0;" v-on:click="BookNowCheck()" >Book now</a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Second Row: Search Results -->
            <!-- mt-4 adds some margin-top for spacing -->
            <div class="row mt-4">
                <div class="col-12">
                    <!-- The content of the search results template will go here -->
                    <template v-if="filteredItems.length > 0">
                        <div class="row">
                            <!-- <div class="small-12 medium-4 large-4 columns" v-for="f in paginated('filterResults')" v-if="f.vessel_size_limit >= vesselSize && f.vessel_draft_limit >= vesselDraft && weightBeam(f) == true"> -->
                                <div class="small-12 medium-4 large-4 columns" v-for="f in paginatedItems" :key="f.id">
                                <div class="row">
                                    <div class="small-12 columns">
                                        <span class="searchTitle">{{ f.name }}</span>
                                    </div>
                                    <div class="small-12 medium-12 large-12 columns" >
                                        <img v-if="f.images[0]" class="thumbnail" v-bind:src="f.images[0].image" style='width: 230px; height: 230px;' />
                                        <img v-else class="thumbnail" src="@/assets/mooring_photo_scaled.png" style='width: 230px; height: 230px;'/>
                                    </div>
                                    <div class="small-12 medium-9 large-9 columns">
                                        <div v-html="f.description"/>
                                        <p v-if="f.price_hint && Number(f.price_hint)"><i><small>From ${{ f.price_hint }} per night</small></i></p>
                                        <!-- <p style='display:none'><i><small>Vessel Size Limit: {{ f.vessel_size_limit }} </small></i></p>
                                        <p ><i><small>Max Stay Period: {{ f.max_advance_booking }} day/s </small></i></p> -->
                                        <p>Mooring Limits</p>
                                        <div class="row">
                                            <div class="col-md-6"  style='display:none'>
                                                <small>Max Stay: {{ f.max_advance_booking }} day/s</small>
                                            </div>
                                            <div class="col-md-6">
                                                <small>Max Size: {{ f.vessel_size_limit }}</small>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6">
                                                <small>Max Draft: {{ f.vessel_draft_limit }}</small>
                                            </div>
                                            <div class="col-md-6">
                                                <small v-if="f.mooring_physical_type == 0"> Max Weight: {{ f.vessel_weight_limit }}</small>
                                                <small v-else> Max Beam: {{ f.vessel_beam_limit }}</small>
                                            </div>
                                        </div>

                                        <a class="button" v-bind:href="f.info_url" target="_blank">More info</a>
                                            
                                        <a v-if="f.mooring_type == 0 && vesselSize > 0 && vesselDraft > 0 && vesselWeight > 0 && vesselRego != '' && vesselRego !== ' '" class="button" v-bind:href="parkstayUrl+'/availability2/?site_id='+f.id+'&'+bookingParam">Book now</a>
                                        <a v-else-if="f.mooring_type == 1 && vesselSize > 0 && vesselDraft > 0 && vesselBeam > 0 && vesselRego != '' && vesselRego !== ' '" class="button" v-bind:href="parkstayUrl+'/availability2/?site_id='+f.id+'&'+bookingParam">Book now</a>
                                        <a v-else-if="f.mooring_type == 2 && vesselSize > 0 && vesselDraft > 0 && vesselBeam > 0 && vesselRego != '' && vesselRego !== ' '" class="button" v-bind:href="parkstayUrl+'/availability2/?site_id='+f.id+'&'+bookingParam">Book now</a>
                                        <a v-else-if="f.mooring_type == 0" class="button" v-on:click="BookNow('mooring')">Book now</a>
                                        <a v-else-if="f.mooring_type == 1 || f.mooring_type == 2 " class="button" v-on:click="BookNow('jettybeach')">Book now</a>
                                        <a v-else /> 
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row text-center">
                            <div class="button-group">
                                <button class="button" @click="prevPage" :disabled="currentPage === 1">
                                « Prev
                                </button>
                                <span class="button secondary disabled">
                                Page {{ currentPage }} / {{ totalPages }}
                                </span>
                                <button class="button" @click="nextPage" :disabled="currentPage === totalPages">
                                Next »
                                </button>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        <div class="row align-center">
                            <div class="small-12 medium-12 large-12 columns">
                                <h2 class="text-center">There are no moorings found matching your search criteria. Please change your search query.</h2>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// CSS files for Foundation and its plugins
// import 'foundation-sites/dist/css/foundation.min.css';
// import 'foundation-datepicker/css/foundation-datepicker.min.css';

// JS files for Foundation and its plugins
// Thanks to ProvidePlugin, we don't need to import jQuery here.
// import 'foundation-sites';
// import 'foundation-datepicker/js/foundation-datepicker'; // Adjust path if needed

import Awesomplete from 'awesomplete';


// import ol from 'openlayers';
import Map from 'ol/Map'
import { get as getProjection } from 'ol/proj';
import { getWidth, getTopLeft } from 'ol/extent';
import WMTSTileGrid from 'ol/tilegrid/WMTS';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import WMTS from 'ol/source/WMTS';
import GeoJSON from 'ol/format/GeoJSON';
import Collection from 'ol/Collection';
import VectorSource from 'ol/source/Vector';
import Overlay from 'ol/Overlay';
import Feature from 'ol/Feature';
import { Style, Icon, Text, Fill, Stroke } from 'ol/style';
import View from 'ol/View';
import { defaults as defaultControls, ScaleLine, Zoom } from 'ol/control';
import { defaults as defaultInteractions, PinchZoom } from 'ol/interaction';
import Geolocation from 'ol/Geolocation';
import { transform, METERS_PER_UNIT, fromLonLat, toLonLat } from 'ol/proj';
import Point from 'ol/geom/Point';

import debounce from 'debounce';
import moment from 'moment';
import swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.css';

import sitesOnlineIcon from '@/assets/pin.svg';
import sitesInPersonIcon from '@/assets/pin_offline.svg';
import sitesAltIcon from '@/assets/pin_alt.svg';
import locationIcon from '@/assets/location.svg';
import boatingFont from '@/assets/fonts/boating.woff';

import iconDefault from '@/assets/map_pins/geo_group_red.png';
import icon30Plus from '@/assets/map_pins/geo_group2.png';
import icon10Plus from '@/assets/map_pins/geo_group_orange.png';

import pin_orange from '@/assets/map_pins/pin_orange.png';
import pin_orange_red from '@/assets/map_pins/pin_orange_red.png';
import pin_red from '@/assets/map_pins/pin_red.png';
import pin_gray from '@/assets/map_pins/pin_gray.png';

var nowTemp = new Date();
var now = moment.utc({year: nowTemp.getFullYear(), month: nowTemp.getMonth(), day: nowTemp.getDate(), hour: 0, minute: 0, second: 0}).toDate();
var fivedays = new Date();
fivedays.setDate(fivedays.getDate() + 5);
fivedays = moment.utc({year: fivedays.getFullYear(), month: fivedays.getMonth(), day: fivedays.getDate(), hour: 0, minute: 0, second: 0}).toDate();

export default {
    name: 'parkfinder',
    el: '#parkfinder',
    props: {
        dataSourceUrl: {
            type: String,
            required: true,
        }
    },
    data: function () {
        return {
            parkstayUrl: '',
            defaultCenter: [13775786.985667605, -2871569.067879858], // [123.75, -24.966],
            defaultLayers: [
                ['dpaw:mapbox_outdoors', {}],
                ['cddp:dpaw_tenure', {}],
            ],
            filterList: [
            ],
            extraFilterList: [
                {name: 'Bookable Mooring', symb: 'MAINS', key: 'jettpenn', 'remoteKey': ['POWERED SITES']},
                {name: 'Non Bookable Mooring', symb: 'MAINS', key: 'mooring', 'remoteKey': ['POWERED SITES']},
            ],
            hideExtraFilters: true,
            suggestions: {},
            extentFeatures: [],
            arrivalDate: now,
            departureDate: fivedays,
            dateCache: null,
            numAdults: 2,
            numConcessions: 0,
            numChildren: 0,
            numInfants: 0,
            numMooring: 1,
            gearType: 'all',
            penType: 'all',
            filterParams: {
            },
            dateSetFirstTime: true,
            sitesOnline: true,
            sitesInPerson: true,
            sitesAlt: true,
            sitesOnlineIcon: sitesOnlineIcon,
            sitesInPersonIcon: sitesInPersonIcon,
            sitesAltIcon: sitesAltIcon,
            locationIcon: locationIcon,
            boatingFont: boatingFont,
            paginate: ['filterResults'],
            selectedFeature: null,
            current_map_scale: 1950001,
            anchorPins: null,
            anchorGroups: {},
            anchorPinsActive: [],
            vesselRego: '',
            vesselSize: 0,
            vesselDraft: 0,
            vesselBeam: 0,
            vesselWeight: 0,
            groupPinLevelChange: true,
            anchorPinLevelChange: true,
            mooring_map_data: null,
            markerAvail: [],
            current_booking: [],
            total_booking: "0.00",
            timer: -1,
            expiry: null,
            booking_expired_notification: false,
            ongoing_booking: false,
            admissions_key: null,
            pinsCache:{},
            mapLoading: false,
            loadingID: 0,

            // For custom pagination.  vue-paginate cannot be used with Vue3
            currentPage: 1,
            itemsPerPage: 9,

            pin_orange: pin_orange,
            pin_orange_red: pin_orange_red,
            pin_red: pin_red,
            pin_gray: pin_gray, 
        }
    },
    computed: {
        // --- Translator for Arrival Date ---
        arrivalDateForInput: {
            /**
             * GET: Formats the internal Date object into a 'YYYY-MM-DD' string
             * for the <input type="date"> element.
             */
            get() {
                return this.formatDateForInput(this.arrivalDate);
            },
            /**
             * SET: Parses the 'YYYY-MM-DD' string from the input
             * back into a Date object to update the internal state.
             */
            set(value) {
                // value is a string like '2023-10-27' from the input
                this.arrivalDate = new Date(value + 'T00:00:00'); // Use T00:00:00 to avoid timezone shifts

                // --- Validation Logic ---
                // If the new arrival date makes the departure date invalid, reset it.
                if (this.departureDate && this.departureDate <= this.arrivalDate) {
                    // ...then automatically set the departure date to the day AFTER the new arrival date.
                    const nextDay = new Date(this.arrivalDate);
                    nextDay.setDate(nextDay.getDate() + 1);
                    this.departureDate = nextDay;
                }
            }
        },
        // --- Translator for Departure Date ---
        departureDateForInput: {
            get() {
                return this.formatDateForInput(this.departureDate);
            },
            set(value) {
                this.departureDate = value ? new Date(value + 'T00:00:00') : null;
            }
        },
        // --- Dynamic 'min' attributes for the inputs ---
        minArrivalDateForInput() {
            return this.formatDateForInput(new Date());
        },
        minDepartureDateForInput() {
            if (!this.arrivalDate) {
                return this.minArrivalDateForInput;
            }
            const nextDay = new Date(this.arrivalDate);
            nextDay.setDate(nextDay.getDate() + 1);
            return this.formatDateForInput(nextDay);
        },
        bookableOnly: {
            cache: false,
            get: function() {
                return this.sitesOnline && (!this.sitesInPerson) && (!this.sitesAlt);
            },
            set: function(val) {
                this.sitesOnline = true;
                this.sitesInPerson = !val;
                this.sitesAlt = !val;
                // this.reload();
            }
        },
        extent: {
            cache: false,
            get: function() {
                return this.olmap.getView().calculateExtent(this.olmap.getSize());
            }
        },
        center: {
            cache: false,
            get: function() {
                return this.olmap.getView().getCenter();
            }
        },
        arrivalDateString: {
            cache: false,
            get: function() {
                // return this.arrivalEl[0].value ? moment(this.arrivalData.getDate()).format('YYYY/MM/DD') : null; 
                return this.arrivalEl[0].value ? moment(this.arrivalDate).format('YYYY/MM/DD') : null; 
            }
        },
        departureDateString: {
            cache: false,
            get: function() {
                // return this.departureEl[0].value ? moment(this.departureData.getDate()).format('YYYY/MM/DD') : null; 
                return this.departureEl[0].value ? moment(this.departureDate).format('YYYY/MM/DD') : null; 
            }
        },
        numPeople: {
            cache: false,
            get: function() {
                // var count = this.numAdults + this.numConcessions + this.numChildren + this.numInfants + this.numMooring;
                var count = this.numAdults + this.numConcessions + this.numChildren + this.numInfants;
                if (count === 1) {
                    return count +" person ▼";
                } else {
                    return count + " people ▼";
                }
            }
        },
        timeleft: {
                cache: false,
                get: function() {
                    // Minutes and seconds
                    var mins = ~~(this.timer / 60);
                    var secs = this.timer % 60;

                    // Hours, minutes and seconds
                    var hrs = ~~(this.timer / 3600);
                    var mins = ~~((this.timer % 3600) / 60);
                    var secs = this.timer % 60;

                    // Output like "1:01" or "4:03:59" or "123:03:59"
                    var ret = "";

                    if (hrs > 0) {
                        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
                    }

                    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
                    ret += "" + secs;
                    if (this.ongoing_booking) {
                       if (this.timer < 0) {
                            if (this.booking_expired_notification == false) {
                           console.log('TIMED OUT');
                           clearInterval(this.timer);
                           this.bookingExpired();
                           this.booking_expired_notification = true;
                        }
                       }
                    }
                    return ret;
                }
        },
        bookingParam: {
            cache: false,
            get: function() {
                if (this.vesselSize % 1 != 0){
                    this.vesselSize = parseFloat(this.vesselSize);
                }
                if (this.vesselDraft % 1 != 0){
                    this.vesselDraft = parseFloat(this.vesselDraft);
                }
                if (this.vesselBeam % 1 != 0){
                    this.vesselBeam = parseFloat(this.vesselBeam);
                }
                if (this.vesselWeight % 1 != 0){
                    this.vesselWeight = parseFloat(this.vesselWeight);
                }
                var params = {
                    'num_adult': this.numAdults,
                    'num_children': this.numChildren,
                    'num_infant': this.numInfants,
                    'num_mooring' : this.numMooring,
                    'gear_type': this.gearType,
                    'pen_type': this.penType,
                    'vessel_size' : this.vesselSize,
                    'vessel_draft': this.vesselDraft,
                    'vessel_beam': this.vesselBeam,
                    'vessel_weight': this.vesselWeight,
                    'vessel_rego': this.vesselRego,
                };
                if (this.arrivalDate && this.departureDate) {
                    params['arrival'] = this.arrivalDateString;
                    params['departure'] = this.departureDateString;
                }
                return $.param(params);
            }
        },
        /**
         * @computed
         * Filters the master list based on current criteria.
         * This computed property accomplishes two things:
         * 1. It safely handles `null` or `undefined` entries in the source array, fixing the error.
         * 2. It centralizes the filtering logic that was previously in the template's `v-if`.
         * @returns {Array} A clean, filtered array of items.
         */
        filteredItems() {
            // A guard clause to prevent errors if `extentFeatures` is not yet loaded.
            if (!this.extentFeatures) {
                return [];
            }

            return this.extentFeatures.filter(f => {
                // Primary guard: ensures 'f' is a valid object, preventing the original error.
                if (!f) {
                    return false;
                }

                // The filtering logic, moved here from the old `v-if` directive.
                const sizeCondition = f.vessel_size_limit >= this.vesselSize;
                const draftCondition = f.vessel_draft_limit >= this.vesselDraft;
                const weightCondition = this.weightBeam(f) === true;

                return sizeCondition && draftCondition && weightCondition;
            });
        },

        /**
         * @computed
         * Slices the filtered list to get only the items for the current page.
         * This is the array you will loop through in your template.
         * @returns {Array} The items to be displayed on the current page.
         */
        paginatedItems() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            
            // `slice` returns a new array containing the elements for the current page.
            return this.filteredItems.slice(startIndex, endIndex);
        },

        /**
         * @computed
         * Calculates the total number of pages based on the filtered item count.
         * Used to build the pagination control UI.
         * @returns {number} The total number of pages.
         */
        totalPages() {
            // Calculates total pages, ensuring it's at least 1.
            return Math.ceil(this.filteredItems.length / this.itemsPerPage) || 1;
        }
    },
    watch: {
        // Watch for changes in filter criteria and reset to the first page.
        // This prevents being on a non-existent page (e.g., page 5) after a filter
        // reduces the total pages to 3.
        vesselSize() {
            this.currentPage = 1;
        },
        vesselDraft() {
            this.currentPage = 1;
        }
    },
    methods: {
        /**
         * A helper function to format a Date object into 'YYYY-MM-DD' string
         * for the <input type="date"> element.
         * @param {Date} date - The input date.
         * @returns {string} - The formatted date string.
         */
        formatDateForInput: function(date) {
            if (!date) return '';
            // `get...()` methods are based on the local timezone, which is what users see.
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        searchRego: function(){
            let vm = this;
            vm.vesselRego = vm.vesselRego.replace(/ /g, "");
            vm.vesselRego = vm.vesselRego.toUpperCase();
            vm.vesselRego = vm.vesselRego.replace(/\s/g,"");
            vm.vesselRego = vm.vesselRego.replace(/\W/g,"");
            

            var reg = vm.vesselRego;
            var data = {
                'vessel_rego': reg
            }
            if(reg){
                $.ajax({
                    //url: process.env.VUE_APP_PARKSTAY_URL + "/api/registeredVessels/",
                    url: "/api/get_vessel_info/",
                    dataType: 'json',
                    data: data,
                    method: 'GET',
                    success: function(data, stat, xhr) {
                        if(data['vessel_info']){
                            vm.vesselWeight =  parseFloat(data['vessel_info'].vessel_weight);
                            vm.vesselBeam = parseFloat(data['vessel_info'].vessel_beam);
                            vm.vesselSize = parseFloat(data['vessel_info'].vessel_size);
                            vm.vesselDraft = parseFloat(data['vessel_info'].vessel_draft);
                            $("#vesselSize").val(data['vessel_info'].vessel_size);
                            $("#vesselWeight").val(data['vessel_info'].vessel_weight);
                            $("#vesselBeam").val(data['vessel_info'].vessel_beam);
                            $("#vesselDraft").val(data['vessel_info'].vessel_draft);
                            vm.removePinAnchors();
                            vm.removePinGroups();

                            vm.buildmarkers();

                        } else {
                            console.log("Registration was not found.");
                        }
                    }
                });
            } else {
                vm.vesselWeight = 0;
                vm.vesselBeam = 0;
                vm.vesselSize = 0;
                vm.vesselDraft = 0;
            }
        },
        weightBeam: function(f){
            if (f.mooring_physical_type == 0){
                if (f.vessel_weight_limit >= this.vesselWeight){
                    return true;
                } else {
                    return false;
                }
            } else {
                if (f.vessel_beam_limit >= this.vesselBeam){
                    return true;
                } else {
                    return false;
                }
            }
        },
        bookingExpired: function() {
            swal.fire({
                title: 'Booking Expired',
                text: "Please click start again to begin booking again:",
                type: 'warning',
                showCancelButton: false,
                confirmButtonText: 'Start Again',
                showLoaderOnConfirm: true,
                allowOutsideClick: false
            }).then((value) => {
                    var loc = window.location;
                    window.location = loc.protocol + '//' + loc.host + '/map/';
            });
        },
        toggleShowFilters: function() {
            this.hideExtraFilters = !this.hideExtraFilters;
        },
        search: function(place) {
            if (!place) {
                return;
            }

            var vm = this;
            // search through the autocomplete list first
            var target = this.suggestions['features'].find(function (el) {
                return el['properties']['name'] == place;
            });
            if (target) {
                var view = this.olmap.getView();
                // zoom slightly closer in for campgrounds
                var resolution = vm.resolutions[10];
                if (target['properties']['type'] == 'MooringArea') {
                    resolution = vm.resolutions[14];
                }
                if ('zoom_level' in target['properties']) {
                    var zoom_level = target['properties']['zoom_level'];
                    if (zoom_level > 0) {
                        resolution = vm.resolutions[target['properties']['zoom_level']];
                    }
                }

                // pan to the spot, zoom slightly closer in for campgrounds
                view.animate({
                    center: fromLonLat(target['coordinates']),
                    resolution: resolution,
                    duration: 1000
                });

                // Open the popup
                /*let feature = this.groundsData.a.find(f => parseInt(f.a) == parseInt(target.properties.id));
                if (feature) {
                    setTimeout(() => {
                        vm.popup.setPosition(feature.getGeometry().getCoordinates());
                        // really want to make vue.js render this, except reactivity dies
                        // when you pass control of the popup element to OpenLayers :(
                        $("#mapPopupName")[0].innerHTML = feature.get('name');
                        if (feature.get('images')) {
                            $("#mapPopupImage").attr('src', feature.get('images')[0].image);
                            $("#mapPopupImage").show();
                        } else {
                            $("#mapPopupImage").hide();
                        }
                        if (feature.get('price_hint') && Number(feature.get('price_hint'))) {
                            $("#mapPopupPrice")[0].innerHTML = '<small>From $' + feature.get('price_hint') + ' per night</small>';
                        } else {
                            $("#mapPopupPrice")[0].innerHTML = '';
                        }
                        $("#mapPopupDescription")[0].innerHTML = feature.get('description');
                        $("#mapPopupInfo").attr('href', feature.get('info_url'));
                        $("#mapPopupBook").attr('href', vm.parkstayUrl+'/availability2/?site_id='+feature.getId()+'&'+vm.bookingParam);
                        if (feature.get('campground_type') == 0) {
                            $("#mapPopupBook").show();
                        } else {
                            $("#mapPopupBook").hide();
                        }
                    },1000);
                }*/
                return;
            }

            console.log('Load search');
            // no match, forward on to mapbox geocode query
            var center = toLonLat(vm.center);
            $.ajax({
                url: 'https://mapbox.dpaw.wa.gov.au/geocoding/v5/mapbox.places/'+encodeURIComponent(place)+'.json?'+ $.param({
                    country: 'au',
                    proximity: ''+center[0]+','+center[1],
                    bbox: '112.920934,-35.191991,129.0019283,-11.9662455',
                    types: 'region,postcode,place,locality,neighborhood,address'
                }),
                dataType: 'json',
                success: function(data, status, xhr) {
                    if (data.features && data.features.length > 0) {
                        var view = vm.olmap.getView();
                        view.animate({
                            center: fromLonLat(data.features[0].geometry.coordinates),
                            resolution: vm.resolutions[12],
                            duration: 1000
                        });
                    }
                }
            })
        },
        refreshPopup: function() {
            let vm = this;
            let feature = vm.selectedFeature;
            if (feature != null) {
                vm.popup.setPosition(feature.getGeometry().getCoordinates());
                // really want to make vue.js render this, except reactivity dies
                // when you pass control of the popup element to OpenLayers :(
                $("#mapPopupName")[0].innerHTML = feature.get('name');
                if (feature.get('images')) {
                    $("#mapPopupImage").attr('src', feature.get('images')[0].image);
                    $("#mapPopupImage").show();
                } else {
                    $("#mapPopupImage").hide();
                }
                if (feature.get('price_hint') && Number(feature.get('price_hint'))) {
                    $("#mapPopupPrice")[0].innerHTML = '<small>From $' + feature.get('price_hint') + ' per night</small>';
                } else {
                    $("#mapPopupPrice")[0].innerHTML = '';
                }
                $("#mapPopupDescription")[0].innerHTML = feature.get('description');
                $("#mapPopupInfo").attr('href', feature.get('info_url'));
                $("#mapPopupBook").attr('href', vm.parkstayUrl+'/availability2/?site_id='+feature.getId()+'&'+vm.bookingParam);
                if (feature.get('campground_type') == 0) {
                    $("#mapPopupBook").show();
                } else {
                    $("#mapPopupBook").hide();
                }
            }
        },
        groundFilter: function(feature) {
            return true;
        },
        updateViewport: function(runNow) {
            var vm = this;
            var updateViewportFunc = function() {
                // this object is going to be hammered by vue.js introspection, strip openlayers stuff
               
                vm.extentFeatures = vm.groundsSource.getFeaturesInExtent(vm.extent).filter(vm.groundFilter).map(function (el) {
                    var props = el.getProperties(); 
                    props.style = undefined;
                    props.geometry = props.geometry.getCoordinates();
                    props.distance = Math.sqrt(Math.pow(props.geometry[0]-vm.center[0], 2) + Math.pow(props.geometry[1]-vm.center[1], 2));
                    props.id = el.getId();
                    return props;
                }).sort(function (a, b) {
                    /* distance from map center sort */
                    if (a.distance < b.distance) {
                        return -1;
                    }
                    if (a.distance > b.distance) {
                        return 1;
                    }
                    return 0;

                    /* alphabet sort
                    var nameA = a.name.toUpperCase();
                    var nameB = b.name.toUpperCase();
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }
                    return 0; */
                });
            };
            if (runNow) {
                updateViewportFunc();
            } else {
                if (!vm._updateViewport) {
                    vm._updateViewport = debounce(function() {
                        updateViewportFunc();
                    }, 100);
                }
                vm._updateViewport();
            }
        },
        updateDates: function(ev) {
            // for the first time someone changes the dates, enable the
            // "Show bookable campsites only" flag
            if (this.dateSetFirstTime) {
                this.dateSetFirstTime = false;
                this.bookableOnly = true;
            }
            // this.reload();
        },
        reload: debounce(function () {
            this.groundsSource.loadSource();
            this.anchorPinLevelChange = true;
            this.buildmarkers();
        }, 250),
        removePinGroups: function() {
            // A guard clause to ensure the map object is available.
            const map = this.olmap;
            if (!map) {
                return;
            }

            const layers = map.getLayers();
            
            // Loop backwards through the layers array.
            // This is the standard, safest way to remove items from a collection
            // while iterating over it, as it avoids issues with changing array indices.
            // This eliminates the need for recursion (`this.removePinGroups()`).
            for (let i = layers.getLength() - 1; i >= 0; i--) {
                const layer = layers.item(i);
                
                if (layer.get('markerGroup') === 'circle') {
                    // Remove the layer directly from the map.
                    map.removeLayer(layer);
                }
            }
        },
        removePinAnchors: function() {
            // return false;
            // this.pinsCache = {};
            var layerRemoved = false;
            const map = this.olmap;
            const layers = map.getLayers();
    
            // Use the backwards-looping for rubustness
            for (let i = layers.getLength() - 1; i >= 0; i--) {
                const layer = layers.item(i);
                
                if (layer.get('markerGroup') === 'anchor') {
                    // map.removeLayer(layer);
                    layer.setVisible(false)
                }
            }

            if (layerRemoved == true) {
                // We do this because when we call map.removeLayer it causes the layer
                // to go out of sync resulting in pins not being removed as foreach loop is
                // changed.  This loop ensure all pins have been removed

                // this.removePinAnchors();
            }
            return layerRemoved;
        },
        toggleMap: function(current_selection) {
            var vm = this;
            var map = this.olmap;
            map.getLayers().forEach(function (layer) {
                var name = layer.get('name');
                if (name != undefined) {
                    var visible = layer.getVisible();
                    if (visible == false) {
                        layer.setVisible(true);
                    }
                    if (visible == true) {
                        layer.setVisible(false);
                    }
                }
            });
            if (current_selection == 'satellite') {
                $('#satellite-toggle').hide();
                $('#map-toggle').show();
            } else {
                $('#satellite-toggle').show();
                $('#map-toggle').hide();
            }
        },
        updateFilter: function() {
            var vm = this;
            // make a lookup table of campground features to filter on
            var legit = new Set();
            var filterCb = function (el) {
                if (vm.filterParams[el.key] === true) {
                    for (var i = 0; i < el.remoteKey.length; i++) {
                         legit.add(el.remoteKey[i]);
                    }                  
                }
            };
            this.filterList.forEach(filterCb);
            this.extraFilterList.forEach(filterCb);
            this.groundsFilter.clear();
            this.groundsData.forEach(function (el) {
                // first pass filter against the list of IDs returned by search
                var campgroundType = el.get('mooring_type');
                switch (campgroundType) {
                    case 0:
                    if (!vm.sitesOnline) {
                        return;
                    }
                    break;
                    case 1: 
                    if (!vm.sitesInPerson) {
                        return;
                    }
                    break;
                    case 2:
                    if (!vm.sitesAlt) {
                        return;
                    }
                    break;
                    default:
                    break;
                }
                if (vm.groundsIds.has(el.getId())) {
                    if (legit.size) { // if we have a feature filter list
                        // check that all parameters are present
                        var feats = new Set(el.get('features').map(function(x) {
                            return x.name;
                        }));
                        for (var x of legit) {
                            if (!feats.has(x)) {
                                return;     // missing a feature!
                            }
                        }
                        vm.groundsFilter.push(el);

                    } else {  // no features, return all results
                        vm.groundsFilter.push(el);
                    }
                }
            });
            this.updateViewport(true);
        },
        buildmarkers: function() {
            this.removePinAnchors();
            this.removePinGroups();
            var vm = this;
            var scale = Math.floor(this.current_map_scale);
            var map = this.olmap;
            var mooring_type =  $("input:radio[name=gear_type]:checked").val(); 

            if (scale >= 0 && scale <= 1300000) {
            
            if (vm.groupPinLevelChange == true) { 
                this.removePinGroups(); 
            }

            vm.groupPinLevelChange = false;
            vm.anchorPinLevelChange = true;

            if (vm.anchorPins == null) {  
                 var response = this.mooring_map_data;
                 vm.anchorPins = response; 
            }
           
            var response = vm.anchorPins;
            var pin_count = 0;
            for (var x in response) {
                var mooring = response[x];
                for (var m in mooring) {
                    for (var b in response[x][m]) {
		        if (b == 'geometry') {
                            var vessel_size = $("#vesselSize").val();
                            var vessel_draft = $("#vesselDraft").val();
                            var vessel_beam = $("#vesselBeam").val();
                            var vessel_weight = $("#vesselWeight").val();
                            var type_filter = $("input[name=pen_type]:checked").val();
                            var show_marker = true;
                            if (response[x][m]['properties']['vessel_size_limit'].length == 0) { 
                                response[x][m]['properties']['vessel_size_limit'] = 0;
                            }

                          
                            if (response[x][m]['properties']['mooring_physical_type'] == 0) { 
                                     if (parseFloat(vessel_size) > 0) {
                                         show_marker = false;
                                         if (parseFloat(response[x][m]['properties']['vessel_size_limit']) >= parseFloat(vessel_size)) {
                                             show_marker = true;
                                         }
                                     }

                                     if (parseFloat(vessel_draft) > 0) {
                                         if (show_marker == true) { 
                                            show_marker = false;
                                            if (parseFloat(response[x][m]['properties']['vessel_draft_limit']) >= parseFloat(vessel_draft)) {
                                               show_marker = true;
                                            }
                                         }
                                     }
                                     if (parseFloat(vessel_weight) > 0) {
                                         if (show_marker == true) {
                                            show_marker = false;
                                            if (parseFloat(response[x][m]['properties']['vessel_weight_limit']) >= parseFloat(vessel_weight)) {
                                               show_marker = true;
                                            }
                                         }
                                     }

                            } else if (response[x][m]['properties']['mooring_physical_type'] == 1 || response[x][m]['properties']['mooring_physical_type'] == 2) { 
                                     if (parseFloat(vessel_size) > 0) {
                                         show_marker = false;
                                         if (parseFloat(response[x][m]['properties']['vessel_size_limit']) >= parseFloat(vessel_size)) {
                                             show_marker = true;
                                         }
                                     }
                                     if (parseFloat(vessel_draft) > 0) {
                                         if (show_marker == true) {
                                             show_marker = false;
                                             if (parseFloat(response[x][m]['properties']['vessel_draft_limit']) >= parseFloat(vessel_draft)) {
                                                 show_marker = true;
                                             }
                                         }
                                     }
                                     if (parseFloat(vessel_beam) > 0) {
                                         if (show_marker == true) {
                                            show_marker = false;
                                            if (parseFloat(response[x][m]['properties']['vessel_beam_limit']) >= parseFloat(vessel_beam)) {
                                               show_marker = true;
                                            }
                                         }
                                     }
			    } else {
                                    show_marker = false;
			    }
                            if (show_marker == true) {
                                     if (type_filter == 'all') { 
				     } else { 
                                         show_marker = false;
                                         if (type_filter == 0) {
						if (parseInt(response[x][m]['properties']['mooring_physical_type']) == 0) {
							show_marker = true;
						}
					 }
                                         if (type_filter == 1) {
                                                if (parseInt(response[x][m]['properties']['mooring_physical_type']) == 1) {
                                                        show_marker = true;
                                                }

                                         }
                                         if (type_filter == 2) {
                                                if (parseInt(response[x][m]['properties']['mooring_physical_type']) == 2) {
                                                        show_marker = true;
                                                }

                                         }

                                    }


			    }


                            if (show_marker == true) {
                                var array_search = vm.anchorPinsActive.indexOf(response[x][m]['id']);
  				    if (array_search > 0) {
				    } else {
                                    var marker_id = response[x][m]['id'];
                                    pin_count =  pin_count + 1;
                                    if (response[x][m]['properties']['mooring_type'] == 0) {
                                        if (mooring_type == 'all' || mooring_type == 'rental-available' || mooring_type == 'rental-notavailable') {
                                            if (mooring_type == 'rental-available' || mooring_type == 'rental-notavailable') {
                                                if (this.groundsIds.has(marker_id)) {            
                                                    if (mooring_type == 'rental-available') {
                                                        if (response[x][m]['geometry'] != null ) {
                                                            if (response[x][m]['geometry'].hasOwnProperty('coordinates')) {
                                                                     if (vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]] == null) { 
                                		                     map.addLayer(vm.buildMarkerBookable(response[x][m]['geometry']['coordinates'][0],response[x][m]['geometry']['coordinates'][1],response[x][m]['properties'],response[x][m]['properties']['name'],response[x][m]['id']));
								     } else {
		                                                            var layer2 = vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]];
                		                                            layer2.setVisible(true);
		
                		                                     }

                                                            }
                                                        }
                                                    
                                                    } else {
                                                        if (mooring_type == 'rental-notavailable') {
                                                            // if (this.groundsIds.has(marker_id)) {
                                                            // } else {
                                                            if (response[x][m]['geometry'] != null ) {
                                                                if (response[x][m]['geometry'].hasOwnProperty('coordinates')) {
                                                                   if (vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]] == null) {
                                                                   map.addLayer(vm.buildMarkerBookable(response[x][m]['geometry']['coordinates'][0],response[x][m]['geometry']['coordinates'][1],response[x][m]['properties'],response[x][m]['properties']['name'],response[x][m]['id']));
                                                                   } else {
		                                                            var layer2 = vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]];
                		                                            layer2.setVisible(true);
			
                        		                             }

                                                                }
                                                            }
                                                        }
                                                    }
				                }
                                            } else {
                                                if (response[x][m]['geometry'] != null ) {
                                                    if (response[x][m]['geometry'].hasOwnProperty('coordinates')) {
                                                       if (vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]] == null) {
                                                          map.addLayer(vm.buildMarkerBookable(response[x][m]['geometry']['coordinates'][0],response[x][m]['geometry']['coordinates'][1],response[x][m]['properties'],response[x][m]['properties']['name'],response[x][m]['id']));
                                                       } else {
                                                            var layer2 = vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]];
                                                            layer2.setVisible(true);

                                                     }

                                                    }
                                                }
							                }
                                        }
			            }
 
                                    if (response[x][m]['properties']['mooring_type'] == 1) {
                                        if (mooring_type == 'all') {
                                            if (response[x][m]['geometry'] != null ) {
                                                if (response[x][m]['geometry'].hasOwnProperty('coordinates')) {
                                                    if (vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]] == null) {
                                                        map.addLayer(vm.buildMarkerBookable(response[x][m]['geometry']['coordinates'][0],response[x][m]['geometry']['coordinates'][1],response[x][m]['properties'],response[x][m]['properties']['name'],response[x][m]['id']));
                                                    } else {
                                                        var layer2 = vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]];
                                                        layer2.setVisible(true);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    if (response[x][m]['properties']['mooring_type'] == 2) {
                                        if (mooring_type == 'all' || mooring_type == 'public-notbookable') {
                                            if (response[x][m]['geometry'] != null ) {
                                                if (response[x][m]['geometry'].hasOwnProperty('coordinates')) {
                                                    if (vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]] == null) {
                                                    map.addLayer(vm.buildMarkerNotBookable(response[x][m]['geometry']['coordinates'][0],response[x][m]['geometry']['coordinates'][1],response[x][m]['properties'],response[x][m]['properties']['name'],response[x][m]['id']));
                                                    } else {
                                                        var layer2 = vm.pinsCache[response[x][m]['id']+'-'+vm.markerAvail[response[x][m]['id']]];
                                                        layer2.setVisible(true);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }        
                        }
	        }
	      }
            }
            } else if (scale >= 1300001) {
	        var center = map.getView().getCenter();
            if (center) {
                var latLon = transform([center[0],center[1]], 'EPSG:3857', 'EPSG:4326');
	        }
            if (vm.anchorPinLevelChange == true) { 
                this.removePinAnchors();
	        }
            vm.groupPinLevelChange = true;
            vm.anchorPinLevelChange = false;
            var response = this.mooring_map_data;
            vm.anchorGroups = {};
            var vessel_size = $('#vesselSize').val();
            var vessel_draft = $('#vesselDraft').val();
            var pen_filter = $("input[name=pen_type]:checked").val();
            if (response) { 
                if (response.hasOwnProperty('features')) {

                    var mooring = response['features'];
                    for (var m in mooring) {
                        var mooring_id = response['features'][m]['id'];
                        var mooring_vessel_size = response['features'][m]['properties']['vessel_size_limit'];
                        var mooring_vessel_draft = response['features'][m]['properties']['vessel_draft_limit'];
                        var mooring_physical_type = response['features'][m]['properties']['mooring_physical_type'];
//                        if (mooring_vessel_size >= vessel_size && mooring_vessel_draft >= vessel_draft && this.weightBeam(response['features'][m]['properties']) && ((pen_filter != 'all' && pen_filter == mooring_physical_type) || pen_filter == 'all') && vm.groundsIds['_c'].has(mooring_id)) {
                        if (mooring_vessel_size >= vessel_size && mooring_vessel_draft >= vessel_draft && this.weightBeam(response['features'][m]['properties']) && ((pen_filter != 'all' && pen_filter == mooring_physical_type) || pen_filter == 'all') && vm.groundsIds.has(mooring_id)) {
                            if (vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']] == null) { 
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']] = {};
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['total'] = 1;
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['name'] = response['features'][m]['properties']['park']['district']['region']['name'];
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['zoom_level'] = response['features'][m]['properties']['park']['district']['region']['zoom_level'];
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['geometry'] = response['features'][m]['properties']['park']['district']['region']['wkb_geometry']['coordinates'];
                            } else {
                                vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['total'] = vm.anchorGroups[response['features'][m]['properties']['park']['district']['region']['id']]['total'] + 1;
                            }   
                        }
                    }
                }
            }
            if (Object.keys(vm.anchorGroups).length == 0){
                // vm.removePinGroups();
            } else {
                for (var g in vm.anchorGroups) {
                    var longitude = vm.anchorGroups[g]['geometry'][0];
                    var latitude = vm.anchorGroups[g]['geometry'][1];

                    var total = vm.anchorGroups[g]['total'];
                    var name = vm.anchorGroups[g]['name'];
                    var zoom_level = vm.anchorGroups[g]['zoom_level'];
                    map.addLayer(vm.buildMarkerGroup(parseFloat(longitude),parseFloat(latitude),total,name, zoom_level));
                }
            }
        } else {
            scale = Math.round(scale);
        }
//        document.getElementById('scale').innerHTML = "Scale = 1 : " + scale;
        },
        buildMarkerBookable: function(lat,lon,props,name,marker_id) {
            var vm = this;
            // var mooring_type =  $("input:radio[name=gear_type]:checked").val();
            var pin_type = vm.pin_red
            var bookable = false;
            var vectorLayer;
            if (vm.pinsCache[marker_id] == null) { 
                if (this.groundsIds.has(marker_id)) {
                    if (vm.markerAvail[marker_id] == 'free') { 
                        pin_type = vm.pin_orange
                        bookable = true;
                    } else if (vm.markerAvail[marker_id] == 'partial') {
                        pin_type = vm.pin_orange_red
                        bookable = true;
                    } else {
                        pin_type = vm.pin_red
                        bookable = false;
                    }	
                }
                var iconFeature = new Feature({
                    marker_group: 'mooring_marker',
                    geometry: new Point(transform([lat, lon], 'EPSG:4326', 'EPSG:3857')),
                    name: name,
                    bookable: bookable,
                    marker_id: marker_id,
                    props: props
                });

                var iconStyle = new Style({
                    image: new Icon(/** @type {olx.style.IconOptions} */ ({
                        imgSize: [32, 32],
                        size: [32,32],
                        snapToPixel: true,
                        anchor: [0.5, 1.0],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'fraction',
                        opacity: 0.95,
                        src: pin_type 
                    })),
                });
                iconFeature.setStyle(iconStyle);

                var vectorSource = new VectorSource({
                    features: [iconFeature]
                });
                vectorLayer = new VectorLayer({
                    canDelete: "yes",
                    markerGroup: "anchor",
                    source: vectorSource
                });
                vm.pinsCache[marker_id+'-'+vm.markerAvail[marker_id]] = vectorLayer; 
            } else {
                vectorLayer = vm.pinsCache[marker_id+'-'+vm.markerAvail[marker_id]];
            }
            return vectorLayer;
        },
        buildMarkerNotBookable: function(lat,lon,props,name,marker_id) {
            var vm = this; 
            if (vm.pinsCache[marker_id+'-'+vm.markerAvail[marker_id]] == null) {
                var iconFeature = new Feature({
                    marker_group: 'mooring_marker',
                    geometry: new Point(transform([lat, lon], 'EPSG:4326', 'EPSG:3857')),
                    name: name,
                    population: 4000,
                    rainfall: 500,
                    marker_id: marker_id,
                    props: props
                });

                var iconStyle = new Style({
                    image: new Icon(/** @type {olx.style.IconOptions} */ ({
                        imgSize: [32, 32],
                        size: [32,32], 
                        snapToPixel: true,
                        anchor: [0.5, 1.0],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'fraction',
                        opacity: 0.95,
                        src: vm.pin_gray
                    }))
                });
                iconFeature.setStyle(iconStyle);
        
                var vectorSource = new VectorSource({
                    features: [iconFeature]
                });

                var vectorLayer = new VectorLayer({
                    canDelete: "yes",
                    markerGroup: "anchor",
                    source: vectorSource
                });
                vm.pinsCache[marker_id+'-'+vm.markerAvail[marker_id]] = vectorLayer;
            } else {
                vectorLayer = vm.pinsCache[marker_id+'-'+vm.markerAvail[marker_id]];
            }
            return vectorLayer;
        },
        buildMarkerGroup:function(lat,lon,text, name, zoom_level) {
            var iconFeature = new Feature({
                marker_group: 'group_marker',
                geometry: new Point(transform([lat, lon], 'EPSG:4326', 'EPSG:3857')),
                name: name,
                zoom_level: zoom_level
            });
            
            var icon = iconDefault
            if (text > 30) {
                icon = icon30Plus
            } else if (text > 10) {
                icon = icon10Plus
            } 

            var iconStyle = new Style({
                image: new Icon(/** @type {olx.style.IconOptions} */ ({
                    imgSize: [48, 46],
                    size: [48,46],
                    anchor: [0.5, 24],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    opacity: 15,
                    src: icon
                })),

                text: new Text({
                    text: text.toString(),
                    scale: 1.2,
                    fill: new Fill({
                        color: '#000000'
                    }),
                })
            });
            iconFeature.setStyle(iconStyle);

            var vectorSource = new VectorSource({
                features: [iconFeature]
            });

            var vectorLayer = new VectorLayer({
                canDelete: "yes",
                markerGroup: "circle",
                source: vectorSource
            });

            return vectorLayer;
        },
        deleteBooking: function(booking_item_id) {
            var vm = this;
            var submitData = {
                booking_item: booking_item_id,
            };

            $.ajax({
                url: vm.parkstayUrl + '/api/booking/delete',
                dataType: 'json',
                method: 'POST',
                data: submitData,
                success: function(data, stat, xhr) {
                    vm.updateBooking();
                },
                error: function(xhr, stat, err) {
                    vm.updateBooking();
                }
            });  
        },
        updateBooking: function() {
            var vm = this;
            $.ajax({
                url: vm.parkstayUrl+'/api/current_booking',
                dataType: 'json',
                // async: false,
                success: function (response, stat, xhr) {
                    vm.current_booking = response.current_booking.current_booking;
                    vm.total_booking = response.current_booking.total_price;
                    vm.timer = response.current_booking.timer;
                    vm.ongoing_booking = response.current_booking.ongoing_booking[0];
                    if (response.current_booking.details != null) {  
                        vm.numAdults = parseInt(response.current_booking.details[0].num_adults) > 0 ? parseInt(response.current_booking.details[0].num_adults) : 2;
                        vm.numChildren = parseInt(response.current_booking.details[0].num_children) > 0 ? parseInt(response.current_booking.details[0].num_children) : 0;
                        vm.numInfants =  parseInt(response.current_booking.details[0].num_infants) > 0 ? parseFloat(response.current_booking.details[0].num_infants) : 0;
                        vm.vesselSize = parseFloat(response.current_booking.details[0].vessel_size) > 0 ? parseFloat(response.current_booking.details[0].vessel_size) : 0;
                        vm.vesselDraft = parseFloat(response.current_booking.details[0].vessel_draft) > 0 ? parseFloat(response.current_booking.details[0].vessel_draft) : 0;
                        vm.vesselBeam = parseFloat(response.current_booking.details[0].vessel_beam) > 0 ? parseFloat(response.current_booking.details[0].vessel_beam) : 0;
                        vm.vesselWeight = parseFloat(response.current_booking.details[0].vessel_weight) > 0 ? parseFloat(response.current_booking.details[0].vessel_weight) : 0;
                        vm.vesselRego = response.current_booking.details[0].vessel_rego ? response.current_booking.details[0].vessel_rego : "";
                    }

                }
            });

        },
        BookNowCheck: function() {
            var mooring_type = $('#mapPopupMooringType').val();
            if (mooring_type == 0) { 
                this.BookNow('mooring');
            } else {
                    this.BookNow('jettybeach');
            }
        },
        BookNow: function(mooring_type) { 
            var vessel_size = $('#vesselSize').val();
            var vessel_draft = $('#vesselDraft').val();
            var vessel_beam = $('#vesselBeam').val();
            var vessel_weight = $('#vesselWeight').val();
            var vessel_rego = $('#vesselRego').val();
            if (!(vessel_draft > 0)){
                swal.fire({
                    title: 'Missing Vessel Draft',
                    text: "Please enter vessel draft:",
                    type: 'warning',
                    showCancelButton: false,
                    confirmButtonText: 'OK',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: false
                })
            }
            if (!(vessel_size > 0) ) {
                swal.fire({
                    title: 'Missing Vessel Size',
                    text: "Please enter vessel size:",
                    type: 'warning',
                    showCancelButton: false,
                    confirmButtonText: 'OK',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: false
                })
            }
            if (mooring_type == 'jettybeach') {  
                if (!(vessel_beam > 0)){
                    swal.fire({
                        title: 'Missing Vessel Beam',
                        text: "Please enter vessel beam:",
                        type: 'warning',
                        showCancelButton: false,
                        confirmButtonText: 'OK',
                        showLoaderOnConfirm: true,
                        allowOutsideClick: false
                    })
                }
            }
            if (mooring_type == 'mooring') {
                if (!(vessel_weight > 0)){
                    swal.fire({
                        title: 'Missing Vessel Weight',
                        text: "Please enter vessel weight:",
                        type: 'warning',
                        showCancelButton: false,
                        confirmButtonText: 'OK',
                        showLoaderOnConfirm: true,
                        allowOutsideClick: false
                    })
                }
            }
            if (!vessel_rego || vessel_rego == "" || vessel_rego == " "){
                swal.fire({
                    title: 'Missing Vessel Registration',
                    text: "Please enter a vessel registration.",
                    type: 'warning',
                    showCancelButton: false,
                    confirmButtonText: 'OK',
                    showLoaderOnConfirm: true,
                    allowOutsideClick: false,
                })
            }
        },
        loadMap: function() {
            var vm = this;

            console.log('Loading map...');
            var nowTemp = new Date();
            var now = moment.utc({year: nowTemp.getFullYear(), month: nowTemp.getMonth(), day: nowTemp.getDate(), hour: 0, minute: 0, second: 0}).toDate();

            // load autosuggest choices
            var search = document.getElementById('searchInput');
            var autocomplete = new Awesomplete(search);
            autocomplete.autoFirst = true;

            $.ajax({
                url: vm.parkstayUrl+'/api/search_suggest',
                dataType: 'json',
                success: function (response, stat, xhr) {
                    vm.suggestions = response;
                    $(search).on('awesomplete-selectcomplete', function(ev) {
                        this.blur();
                    });

                    autocomplete.list = response['features'].map(function (el) {
                        return el['properties']['name'];
                    });
                }
            });

            // wire up search box
            $(search).on('blur', function(ev) {
                vm.search(ev.target.value);
            }).on('keypress', function(ev) {
                if (!ev) {
                    ev = window.event;
                }
                // intercept enter keys
                var keyCode = ev.keyCode || ev.which;
                if (keyCode == '13') {
                    this.blur();
                    return false;
                }
            });

            // generate WMTS tile grid
            // this.projection = ol.proj.get('EPSG:3857');
            this.projection = getProjection('EPSG:3857');
            this.projectionExtent = this.projection.getExtent();
            // var size = ol.extent.getWidth(this.projectionExtent) / 256;
            var size = getWidth(this.projectionExtent) / 256;
            this.matrixSet = 'mercator';
            this.resolutions = new Array(21);
            this.matrixIds = new Array(21);
            for (var z = 0; z < 21; ++z) {
                // generate resolutions and matrixIds arrays for this WMTS
                this.resolutions[z] = size / Math.pow(2, z);
                this.matrixIds[z] = this.matrixSet + ':' + z;
            }

            var tileGrid = new WMTSTileGrid({
                origin: getTopLeft(this.projectionExtent),
                resolutions: this.resolutions,
                matrixIds: this.matrixIds
            });
            this.streets = new TileLayer({
                canDelete: "no",
                source: new WMTS({
                    url: vm.dataSourceUrl + '/geoserver/gwc/service/wmts',
                    format: 'image/png',
                    layer: 'kaartdijin-boodja-public:mapbox-streets-public',
                    matrixSet: this.matrixSet,
                    projection: this.projection,
                    tileGrid: tileGrid
                })
            });

            this.geojson = new GeoJSON({
                featureProjection: 'EPSG:3857'
            });

            this.groundsData = new Collection();
            this.groundsIds = new Set();
            this.groundsFilter = new Collection();

            $.ajax({
                url: vm.parkstayUrl+'/api/mooring_map/?format=json',
                dataType: 'json',
                success: function (response, stat, xhr) {
                    var features = vm.geojson.readFeatures(response);
                    vm.groundsData.clear();
                    vm.groundsData.extend(features);
                    vm.groundsSource.loadSource();
                }
            });

            this.groundsSource = new VectorSource({
                features: vm.groundsFilter
            });

            // Marker Popup Code
            $('#mapPopupClose').on('click', function(ev) {
                $('#mapPopup').hide();
                vm.popup.setPosition(undefined);
                vm.selectedFeature = null;
                return false;
            });
            this.popupContent = document.getElementById('mapPopupContent');
            this.popup = new Overlay({
                element: document.getElementById('mapPopup'),
                autoPan: true,
                autoPanAnimation: {
                    duration: 250
                }
            });

            this.posFeature = new Feature();
            this.posFeature.setStyle(new Style({
                image: new Icon({
                    src: vm.locationIcon,
                    snapToPixel: true,
                    anchor: [0.5, 0.5],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'fraction'
                })
            }));

            this.posLayer = new VectorLayer({
                source: new VectorSource({
                    features: [this.posFeature]
                })
            });
            // create OpenLayers map object, prefill with all the stuff we made
            this.olmap = new Map({
                logo: false,
                renderer: 'canvas',
                target: 'map',
                view: new View({
                    projection: 'EPSG:3857',
                    center: vm.defaultCenter,
                    zoom: 5,
                    maxZoom: 21,
                    minZoom: 5
                }),
                controls: [
                    new Zoom(),
                    new ScaleLine(),
                ],
                interactions: defaultInteractions({
                    // This correctly disables rotation interactions.
                    altShiftDragRotate: false,
                    pinchRotate: false
                }).extend([
                    // The original code tried to add a custom PinchZoom.
                    // Note: The default set already includes PinchZoom. `extend` adds another one.
                    // If the goal is to *replace* it, a more advanced pattern is needed.
                    // This corrected code assumes the primary goal was to disable rotation
                    // while keeping other defaults.
                ]),
                layers: [
                    this.streets,
                    this.posLayer
                ],
                overlays: [this.popup]
            });
        },
        weightBeam(f) {
            return true; 
        },
        /**
         * Navigates to the next page if not on the last page.
         */
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        /**
         * Navigates to the previous page if not on the first page.
         */
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        /**
         * Navigates directly to a specific page number.
         * @param {number} pageNumber - The page to go to.
         */
        goToPage(pageNumber) {
            // You could add validation here if needed (e.g., pageNumber > 0 && pageNumber <= this.totalPages)
            this.currentPage = pageNumber;
        }
    },
    mounted: function() {
        this.$nextTick(() => {
            var vm = this;

            var template_group = $('#template_group').val();
            if (template_group == 'rottnest') { 
                vm.admissions_key = 'ria';
            }

            this.arrivalEl = $('#dateArrival');
            this.departureEl = $('#dateDeparture');

            // load autosuggest choices
            var search = document.getElementById('searchInput');
            var autocomplete = new Awesomplete(search);
            autocomplete.autoFirst = true;

            $.ajax({
                url: vm.parkstayUrl+'/api/search_suggest',
                dataType: 'json',
                success: function (response, stat, xhr) {
                    vm.suggestions = response;
                    $(search).on('awesomplete-selectcomplete', function(ev) {
                        this.blur();
                    });

                    autocomplete.list = response['features'].map(function (el) {
                        return el['properties']['name'];
                    });
                }
            });

            // wire up search box
            $(search).on('blur', function(ev) {
                vm.search(ev.target.value);
            }).on('keypress', function(ev) {
                if (!ev) {
                    ev = window.event;
                }
                // intercept enter keys 
                var keyCode = ev.keyCode || ev.which;
                if (keyCode == '13') {
                    this.blur();
                    return false;
                }
            });

            // generate WMTS tile grid
            // this.projection = ol.proj.get('EPSG:3857');
            this.projection = getProjection('EPSG:3857');
            this.projectionExtent = this.projection.getExtent();
            // var size = ol.extent.getWidth(this.projectionExtent) / 256;
            var size = getWidth(this.projectionExtent) / 256;
            this.matrixSet = 'mercator';
            this.resolutions = new Array(21);
            this.matrixIds = new Array(21);
            for (var z = 0; z < 21; ++z) {
                // generate resolutions and matrixIds arrays for this WMTS
                this.resolutions[z] = size / Math.pow(2, z);
                this.matrixIds[z] = this.matrixSet + ':' + z;
            }

            // var tileGrid = new ol.tilegrid.WMTS({
            //     origin: ol.extent.getTopLeft(this.projectionExtent),
            //     resolutions: this.resolutions,
            //     matrixIds: this.matrixIds
            // });
            const tileGrid = new WMTSTileGrid({
                origin: getTopLeft(this.projectionExtent),
                resolutions: this.resolutions,
                matrixIds: this.matrixIds
            });

            this.streets = new TileLayer({
                name: 'street',
                canDelete: "no",
                visible: true,
                source: new WMTS({
                    url: vm.dataSourceUrl + '/geoserver/gwc/service/wmts',
                    format: 'image/png',
                    layer: 'kaartdijin-boodja-public:mapbox-streets-public',
                    matrixSet: this.matrixSet,
                    projection: this.projection,
                    tileGrid: tileGrid
                })
            });

            this.satellite = new TileLayer({
                name: 'satellite',
                canDelete: "no",
                visible: false,
                source: new WMTS({
                    url: vm.dataSourceUrl + '/geoserver/gwc/service/wmts',
                    format: 'image/png',
                    layer: 'kaartdijin-boodja-public:mapbox-satellite-public',
                    matrixSet: this.matrixSet,
                    projection: this.projection,
                    tileGrid: tileGrid
                })
            });

            // this.geojson = new ol.format.GeoJSON({
            //     featureProjection: 'EPSG:3857'   
            // });

            // this.groundsData = new ol.Collection();
            // this.groundsIds = new Set();
            // this.groundsFilter = new ol.Collection();
            this.geojson = new GeoJSON({
                featureProjection: 'EPSG:3857'
            });
            this.groundsData = new Collection();
            this.groundsIds = new Set();
            this.groundsFilter = new Collection();

            $.ajax({
                url: vm.parkstayUrl+'/api/mooring_map/?format=json',
                dataType: 'json',
                success: function (response, stat, xhr) {
                    vm.mooring_map_data = response;
                    var features = vm.geojson.readFeatures(response);
                    vm.groundsData.clear();
                    vm.groundsData.extend(features);
                    // vm.groundsSource.loadSource();
                    vm.buildmarkers();
                }
            });

            vm.updateBooking();
            // this.groundsSource = new ol.source.Vector({
            //     features: vm.groundsFilter   
            // });
            this.groundsSource = new VectorSource({
                features: this.groundsFilter
            });
            // Defines the custom function to fetch and load filtered mooring data from the API into the map's vector source.
            this.groundsSource.loadSource = function (onSuccess) {
                if (vm.dateCache != vm.arrivalDateString+vm.departureDateString+vm.gearType+vm.penType) {
                    vm.mapLoading = true;
                    vm.loadingID = vm.loadingID + 1;
                    vm.removePinAnchors();
                    vm.anchorPinLevelChange = true;

                    var urlBase = vm.parkstayUrl + '/api/mooring_map_filter/?';
                    var params = {format: 'json'};
                    var isCustom = false;

                    if (vm.arrivalDate && vm.departureDate) {
                        isCustom = true;
                        var arrival = vm.arrivalDateString;
                        if (arrival) {
                            params.arrival = arrival;
                        }
                        var departure = vm.departureDateString;
                        if (departure) {
                            params.departure = vm.departureDateString;
                        }
                        params.num_adult = vm.numAdults;
                        params.num_concessions = vm.numConcessions;
                        params.num_children = vm.numChildren;
                        params.num_infant = vm.numInfants;
                        params.num_mooring = vm.numMooring;
                        params.gear_type = vm.gearType;
                        params.pen_type = vm.penType;
                    }
                    
                    let temp = urlBase + $.param(params)

                    $.ajax({
                        loadID: vm.loadingID,
                        url: urlBase + $.param(params),
                        success: function (response, stat, xhr) {
                            vm.groundsIds.clear();
                            response.forEach(function(el) {
                                vm.groundsIds.add(el.id);

                                vm.dateCache = vm.arrivalDateString+vm.departureDateString+vm.gearType+vm.penType;
                                vm.markerAvail[el.id] = el.avail;
                            });

                            vm.updateFilter();
                            vm.buildmarkers();
                            if (vm.loadingID == this.loadID) {
                                vm.mapLoading = false;
                            }
                        },
                        error: function(xhr, stat, err) {
                            if (vm.loadingID == this.loadID) {
                                vm.mapLoading = false;
                            }
                            if (err) {
                                swal.fire({
                                    title: 'Error',
                                    text: "There was an error loading map data please try again.",
                                    type: 'error',
                                    showCancelButton: false,
                                    confirmButtonText: 'Close',
                                    showLoaderOnConfirm: true,
                                    allowOutsideClick: false
                                });
                            }
                        },
                        dataType: 'json'
                    });
                }
            };
            this.grounds = new VectorLayer({
                source: this.groundsSource,
                style: function (feature) {
                    var style = feature.get('style');
                    return style;
                }
            });
            // Marker Popup Code
            $('#mapPopupClose').on('click', function(ev) {
                $('#mapPopup').hide();
                vm.popup.setPosition(undefined);
                vm.selectedFeature = null;
                return false;
            });
            this.popupContent = document.getElementById('mapPopupContent');
            this.popup = new Overlay({
                element: document.getElementById('mapPopup'),
                autoPan: true,
                autoPanAnimation: {
                    duration: 250
                }
            });

            this.posFeature = new Feature();
            this.posFeature.setStyle(new Style({
                image: new Icon({
                    src: vm.locationIcon,
                    snapToPixel: true,
                    anchor: [0.5, 0.5],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'fraction',
                    imgSize: [32, 32] // JM
                })
            }));

            this.posLayer = new VectorLayer({
                source: new VectorSource({
                    features: [this.posFeature]
                })
            });
            // End of Marker Popup Code

            // create OpenLayers map object, prefill with all the stuff we made
            this.olmap = new Map({
                logo: false,
                renderer: 'canvas',
                target: 'map',
                view: new View({
                    projection: 'EPSG:3857',
                    center: vm.defaultCenter,
                    zoom: 5,
                    maxZoom: 21,
                    minZoom: 5
                }),
                controls: [
                    new Zoom(),
                    new ScaleLine()
                ],
                // interactions: ol.interaction.defaults({
                //     altShiftDragRotate: false,
                //     pinchRotate: false,
                // }),
                // interactions: ol.interaction.defaults({}).extend([
                //       new ol.interaction.PinchZoom({
                //           constrainResolution: true
                //        })
                // ]),
                interactions: defaultInteractions({
                    // This correctly disables rotation interactions.
                    altShiftDragRotate: false,
                    pinchRotate: false
                }).extend([
                    // The original code tried to add a custom PinchZoom.
                    // Note: The default set already includes PinchZoom. `extend` adds another one.
                    // If the goal is to *replace* it, a more advanced pattern is needed.
                    // This corrected code assumes the primary goal was to disable rotation
                    // while keeping other defaults.
                ]),
                layers: [
                    this.streets,
                    this.satellite,
                    this.grounds,
                    this.posLayer
                ],
                overlays: [this.popup]
            });

            $('#map-toggle').hide();
            // spawn geolocation tracker
            this.geolocation = new Geolocation({
                tracking: true,
                projection: this.olmap.getView().getProjection()
            });
            this.geolocation.on('change:position', function() {
                var coords = vm.geolocation.getPosition();
                vm.posFeature.setGeometry(coords ? new Point(coords) : null);
            });

            // JASON ADDED
            var map = this.olmap;

            this.olmap.getView().on('change:resolution', function(evt) {
                var resolution = evt.target.get('resolution');
                var units = map.getView().getProjection().getUnits();
                var dpi = 25.4 / 0.28;
                var mpu = METERS_PER_UNIT[units];

                var scale_res = resolution * mpu * 39.37 * dpi;
                vm.current_map_scale = scale_res;
                setTimeout(function() { if (scale_res == vm.current_map_scale) { vm.buildmarkers(); vm.updateViewport(); }}, 400);
            });

            $('#vesselRego').on('blur', function() {
                vm.searchRego();
            });
            $('#vesselSize').on('blur', function() { 
                vm.vesselSize = this.value;
                vm.removePinAnchors();
                vm.removePinGroups();
                vm.buildmarkers();
            });
            $('#vesselDraft').on('blur', function() { 
                vm.vesselDraft = this.value;
                vm.removePinAnchors();
                vm.removePinGroups();
                vm.buildmarkers();
            });
            $('#vesselBeam').on('blur', function() { 
                vm.vesselBeam = this.value;
                vm.removePinAnchors();
                vm.removePinGroups();
                vm.buildmarkers();
            });
            $('#vesselWeight').on('blur', function() { 
                vm.vesselWeight = this.value;
                vm.removePinAnchors();
                vm.removePinGroups();
                vm.buildmarkers();
            });
            $('#vesselDraft').on('blur', function() {
                vm.vesselDraft = this.value;
                vm.removePinAnchors();
                vm.removePinGroups();
                vm.buildmarkers();
            });
            $('#dateArrival').on('change', function() {
                vm.reload();
            });
            $('#dateDeparture').on('change', function() {
                vm.reload();
            });
            $('#vesselSize').val('0');
            $('#vesselDraft').val('0');
    
            // loop to change the pointer when mousing over a vector layer
            this.olmap.on('pointermove', function(ev) {
                if (ev.dragging) {
                    return;
                }
                var result = map.forEachFeatureAtPixel(ev.pixel, function(feature, layer) {
                $('#map').attr('title', feature.get('name'));
                return feature;
                });
                if (result) {
                    if ($('#map').hasClass('click')) { 
                    } else {
                        $('#map').addClass('click', result);
                    }
                } else {
                    $('#map').removeClass('click', result);
                }
                if (!result) {
                    $('#map').removeAttr('title');
                }
            });

            var element = document.getElementById('mapPopup');

            var popup = new Overlay({
                element: element,
                positioning: 'bottom-center',
                stopEvent: false
            });

            map.addOverlay(popup);
            // another loop to spawn the popup on click
            this.olmap.on('singleclick', function(ev) {
                var feature = ev.map.forEachFeatureAtPixel(ev.pixel, 
                    function(feature, layer) {
                        return feature;
                    }
                );

                if (feature) {
                    var geometry = feature.getGeometry();
                    var coord = geometry.getCoordinates();
                    var properties = feature.getProperties();
                    if (properties.marker_group == 'mooring_marker') {
                        $('#mapPopupName').html(properties.props.name);
                        $('#mapPopupInfo').attr('href', properties.props.info_url);
                        if (properties.props.mooring_type == 0 || properties.props.mooring_type == 1 || properties.props.mooring_type == 2) {
                            $('#mapPopupMooringType').val(properties.props.mooring_physical_type);
                            if (properties.bookable == true) { 
                                $('#mapPopupBook').show();
                            } else {
                                $('#mapPopupBook').hide();
                            }
                            $("#mapPopupImage").show();
                            if (properties.props.images.length > 0) { 
                                $("#mapPopupImage").attr('src',  properties.props.images[0].image);
                            } else {
                                $("#mapPopupImage").attr('src',  '/static/exploreparks/mooring_photo_scaled.png');
                            }
                            $("#max_stay_period").html(properties.props.max_advance_booking);
                            $("#vessel_size_popup").html(properties.props.vessel_size_limit);
                            $("#vessel_draft_popup").html(properties.props.vessel_draft_limit);
                            if(properties.props.mooring_physical_type == 0){
                                $("#vessel_beam_weight_popup").html("Max Weight: " + properties.props.vessel_weight_limit);
                            }
                            else {
                                $("#vessel_beam_weight_popup").html("Max Beam: " + properties.props.vessel_beam_limit);
                            }
                            var vessel_size = $('#vesselSize').val();
                            var vessel_draft = $('#vesselDraft').val();
                            var vessel_rego = $('#vesselRego').val();
                            var vessel_beam = $('#vesselBeam').val();
                            var vessel_weight = $('#vesselWeight').val();

                            if (properties.props.mooring_physical_type == 0 && vessel_size > 0 && vessel_draft > 0 && vessel_weight > 0 &&vessel_rego.length > 1) {
                                var distance_radius = properties.props.park.distance_radius;
                                $("#mapPopupBook").attr('href', vm.parkstayUrl+'/availability2/?site_id='+properties.marker_id+'&distance_radius='+distance_radius+'&'+vm.bookingParam);
                            } else if ((properties.props.mooring_physical_type == 1 || properties.props.mooring_physical_type == 2 ) && ( vessel_size > 0 && vessel_draft > 0 && vessel_beam > 0 && vessel_rego.length > 1)) { 
                                var distance_radius = properties.props.park.distance_radius;
                                $("#mapPopupBook").attr('href', vm.parkstayUrl+'/availability2/?site_id='+properties.marker_id+'&distance_radius='+distance_radius+'&'+vm.bookingParam);
                            } else {
                                $("#mapPopupBook").attr('href','javascript:void(0);');
                                $("#mapPopupBook").attr('target','');
                            }
                        } else {
                            $("#max_stay_period").html(properties.props.max_advance_booking);
                            $("#vessel_size_popup").html(properties.props.vessel_size_limit);
                            $("#vessel_draft_popup").html(properties.props.vessel_draft_limit);
                            if(properties.props.mooring_physical_type == 0){
                                $("#vessel_beam_weight_popup").html("Vessel Weight: " + properties.props.vessel_weight_limit);
                            }
                            else {
                                $("#vessel_beam_weight_popup").html("Vessel Beam: " + properties.props.vessel_beam_limit);
                            }   
                            $('#mapPopupBook').hide();
                        }

                        popup.setPosition(coord);

                        $(element).show();

                    } else if (properties.marker_group == 'group_marker') {
                        var view = vm.olmap.getView();
                        var resolution = vm.resolutions[properties.zoom_level];
                        view.animate({
                            center: coord,
                            resolution: resolution,
                            duration: 1000
                        }); 
                    } 
                } else {
                    $(element).hide();
                }
            });

            var x = document.cookie.split('vessel_rego=');
            if(x.length == 2){
                var secondHalf = x[1].split(';');
                var rego = secondHalf[0];
                vm.vesselRego = rego;
                vm.searchRego(rego);
            }

            var saneTz = (0 < Math.floor((vm.expiry - moment.now())/1000) < vm.timer);
            var timer = setInterval(function (ev) {
                // fall back to the pre-encoded timer
                if (!saneTz) {
                    vm.timer -= 1;
                } else {
                    // if the timezone is sane, do live updates
                    // this way unloaded tabs won't cache the wrong time.
                    var newTimer = Math.floor((vm.expiry - moment.now())/1000);
                    vm.timer = newTimer;
                }

                if ((vm.timer <= -1)) {
                    // clearInterval(timer);
                    // var loc = window.location;
                    // window.location = loc.protocol + '//' + loc.host + loc.pathname;
                }
            }, 1000);

            // hook to update the visible feature list on viewport change
            this.olmap.getView().on('propertychange', function(ev) {
                vm.updateViewport();
                vm.buildmarkers();
            });
            this.reload();
        }) // End $nextTick
    }
};
</script>

<style lang="scss">
    [v-cloak] {
        display: none;
    }
    @font-face {
        font-family: "DPaWSymbols";
        // src: url('/static/exploreparks/fonts/boating.woff') format("woff"); 
        src: url('@/assets/fonts/boating.woff') format("woff");
    }

    .symb {
        font-family: "DPaWSymbols";
        font-style: normal;
        font-size: 1.5rem;
    }

    .symb.RC2:before {
        content: "a";
    }

    .symb.RC4:before {
        content: "b";
    }

    .symb.RV10:before {
        content: "c";
    }

    .symb.RG2:before {
        content: "d";
    }

    .symb.RG15:before {
        content: "e";
    }

    .symb.RV2:before {
        content: "f";
    }

    .symb.RF10:before {
        content: "g";
    }

    .symb.RF13:before {
        content: "h";
    }

    .symb.RF15:before {
        content: "i";
    }

    .symb.RF17:before {
        content: "j";
    }

    .symb.RF1:before {
        content: "k";
    }

    .symb.RF6:before {
        content: "l";
    }

    .symb.RF7:before {
        content: "m";
    }

    .symb.RF19:before {
        content: "n";
    }

    .symb.RF8G:before {
        content: "o";
    }

    .symb.RC1:before {
        content: "p";
    }

    .symb.RC3:before {
        content: "q";
    }

    .symb.LOC:before {
        content: "r";
    }

    .symb.RW3:before {
        content: "s";
    }

    .symb.MAINS:before {
        content: "t";
    }

    .symb.RC20:before {
        content: "v";
    }

    .f6inject {

        .search-params hr {
            margin: 0;
        }

        .search-params label {
            cursor: pointer;
            font-size: 0.8em;
        }

        /* filter hiding on small screens */
        @media print, screen and (max-width: 63.9375em) {
            .filter-hide {
                display: none;
            }
        }

        @media print, screen and (min-width: 64em) {
            .filter-button {
                display: none; 
            }
        }

        #map {
            height: 75vh;
        }

        /* set on the #map element when mousing over a feature */
        .click {
            cursor: pointer;
        }

        input + .symb {
            color: #000000;
            transition: color 0.25s ease-out;
        }

        input:checked + .symb {
            color: #2199e8;
        }

        .button.formButton {
            display: block;
            width: 100%;
        }

        .button.selector {
            background-color: #fff;
            border: 1px solid #777;
            border-radius: 4px;
            color: #000;
        }

        .button.selector:hover {
            background-color: #d6eaff;
            border: 1px solid #729fcf;
        }

        .button.selector ~ input:checked {
            color: #fff;
            background-color: #0060c4;
            border: 1px solid #00366e;
        }

        .button.selector:hover ~ input:checked {
            color: #fff;
            background-color: #0e83ff;
            border: 1px solid #004d9f;
        }

        .pagination {
            padding: 0;
            text-align: center;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 1em;
        }

        .pagination .active {
            background: #2199e8;
            color: #fefefe;
            cursor: default;
        }

        .pagination li {
            display: inline-block;
            cursor: pointer;
        }

        .tooltip {
            position: relative;
            border-radius: 4px;
            background-color: #ffcc33;
            color: black;
            padding: 4px 8px;
            opacity: 0.7;
            white-space: nowrap;
        }

        .tooltip:before {
            border-top: 6px solid rgba(0, 0, 0, 0.5);
            border-right: 6px solid transparent;
            border-left: 6px solid transparent;
            content: "";
            position: absolute;
            bottom: -6px;
            margin-left: -7px;
            left: 50%;
        }

        .mapPopup {
            position: absolute;
            background-color: white;
            -webkit-filter: drop-shadow(0 1px 4px rgba(0,0,0,0.2));
            filter: drop-shadow(0 1px 4px rgba(0,0,0,0.2));
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #cccccc;
            bottom: 32px;
            left: -140px;
            width: 280px;
        }

        .mapPopup:after, .mapPopup:before {
            top: 100%;
            border: solid transparent;
            content: " ";
            height: 0;
            width: 0;
            position: absolute;
            pointer-events: none;
        }

        .mapPopup:after {
            border-top-color: white;
            border-width: 10px;
            left: 138px;
            margin-left: -10px; 
        }

        .mapPopup:before {
            border-top-color: #cccccc;
            border-width: 11px;
            left: 138px;
            margin-left: -11px;
        }

        .mapPopupClose {
            text-decoration: none;
            position: absolute;
            top: 2px;
            right: 8px;
        }

        .mapPopupClose:after {
            content: "✖";
        }

        .searchTitle {
            font-size: 150%;
            font-weight: bold;
        }

        .resultList {
            padding: 0;
        }

        .map-toggle-black {
        width: 80px;
        height: 80px;
        background-color: #FFFFFF;
        color: black;
        position: relative;
        right: 10px;
        top: -90px;
        z-index: 300;
        border: 2px solid #FFFFFF;
        cursor: pointer;
        border-radius: 2px;
        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.3);
        }
        .map-toggle-white {
        width: 80px;
        height: 80px;
        background-color: #FFFFFF;
        color: black;
        position: relative;
        right: 10px;
        top: -90px;
        z-index: 300;
        border: 2px solid #000000;
        cursor: pointer;
        border-radius: 2px;
        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.3);
        }
        .map-loading {
        position: relative;
        top: 14px;
        background-color: #FFFFFF;
        border: 1px solid #bab9b9;
        z-index: 5;
        width: 110px;
        text-align: center;
        opacity: 0.7;
        margin-right: 8px;
        font-size: 12px;
        padding: 4px;
        }
    }

    /* hacks to make awesomeplete play nice with F6 */
    div.awesomplete {
        display: block;
    }

    div.awesomplete > input {
        display: table-cell;
    }

    /* hacks to make openlayers widgets more accessible */
    .ol-control button {
        height: 2em;
        width: 2em;
    }
    .card{
        background-color: #f5f5f5;
        height:40px;
    }
    .card-title{
        margin-top:-7px;
        font-size: 16px;
    }
</style>