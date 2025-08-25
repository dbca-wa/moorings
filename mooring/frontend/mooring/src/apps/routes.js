import Campgrounds from '../components/campgrounds/campgrounds.vue'
import Campground from '../components/campgrounds/campground.vue'
import AddCampground from '../components/campgrounds/addCampground.vue'
// import Campsite from '../components/campsites/campsite.vue'
import firstLevelSearch from '../components/booking/first-level-search.vue'
import bookingDashboard from '../components/booking/dashboard.vue'
// import addBooking from '../components/booking/addbooking.vue'
import BookingIndex from '../components/booking/index.vue'
// import editBooking from '../components/booking/changebooking2.vue'
import page_404 from '../components/utils/404.vue'
import Reports from '../components/reports/reports.vue'
// import Campsite_type_dash from '../components/campsites-types/campsite-types-dash.vue'
// import Campsite_type from '../components/campsites-types/campsite-type.vue'
// import Bulkpricing from '../components/bulkpricing/bulkpricing.vue'
// import booking_periods from '../components/bookingperiods/periods.vue'
import Profile from '../components/user/profile.vue'
import { RouterView} from 'vue-router';

export const routes = [
    {
        path: "/account",
        name: "profile",
        component: Profile
    },
    {
        path:'/dashboard',
        component: RouterView,
        children: [
            // {
            //     path:'campsite-types',
            //     name:'campsite-types',
            //     component: Campsite_type_dash
            // },
            // {
            //     path: 'bookingperiods',
            //     name: 'booking-periods',
            //     component: booking_periods
            // },
            // {
            //     path:'campsite-type',
            //     component: RouterView,
            //     children: [
            //         // {
            //         //     path: '',
            //         //     name: 'campsite-type',
            //         //     component: Campsite_type_dash
            //         // },
            //         // {
            //         //     path:':campsite_type_id',
            //         //     name:'campsite-type-detail',
            //         //     component: Campsite_type,
            //         // }
            //     ]
            // },
            {
                path:'campgrounds/addCampground',
                name:'cg_add',
                component: AddCampground
            },
            {
                path:'moorings',
                component: RouterView,
                children:[
                    {
                        path: '',
                        name: 'cg_main',
                        component: Campgrounds,
                    },
                    {
                        path:':id',
                        name:'cg_detail',
                        component: Campground,
                    },
                    // {
                    //     path:':id/campsites/add',
                    //     name:'add_campsite',
                    //     component:Campsite
                    // },
                    // {
                    //     path:':id/campsites/:campsite_id',
                    //     name:'view_campsite',
                    //     component:Campsite
                    // },
                ]
            },
            {
                path:'bookings',
                component: BookingIndex,
                children:[
                    {
                        path: '',
                        name: 'booking-dashboard',
                        component: bookingDashboard,
                    },
                    // {
                    //     path: 'add/:cg',
                    //     name: 'add-booking',
                    //     component: addBooking,
                    // },
                    // {
                    //     path: 'edit/:booking_id',
                    //     name: 'edit-booking',
                    //     component: editBooking
                    // },
                ]
            },
            // {
            //     path:'bulkpricing',
            //     name:'bulkpricing',
            //     component:Bulkpricing
            // },
            {
                path:'reports',
                name:'reports',
                component:Reports
            },
        ]
    },
    {
        path:'/booking',
        component: RouterView,
        children:[
            {
                path:'',
                name:'fl-search',
                component: firstLevelSearch
            }
        ]
    },
    {
        path: '/404',
        name: '404',
        component: page_404
    }
];