import { sveltekit } from '@sveltejs/kit/vite';
import autoImport from 'sveltekit-autoimport';
import inject from '@rollup/plugin-inject'

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [
		autoImport({
			components: ['./src/components'],
		  }),
		sveltekit(),
		inject({ Buffer: ['buffer', 'Buffer'] })
	],
};

export default config;
